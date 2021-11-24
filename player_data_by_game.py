import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

games = pd.read_csv("./data/nba_games_data/games.csv")
game_details = pd.read_csv("./data/nba_games_data/games_details.csv")
teams = pd.read_csv("./data/nba_games_data/teams.csv")
start_dates = pd.read_csv("./data/season_start.csv")

# Subset tables to only include relevant columns
## Games subset
games_df = games.loc[:, ["GAME_DATE_EST", "GAME_ID", "HOME_TEAM_ID", "TEAM_ID_home", "VISITOR_TEAM_ID",
                  "TEAM_ID_away", "SEASON"]]
games_df = games_df.drop_duplicates(subset="GAME_ID")

# Ensure the two id columns are equivalent
assert len(games_df.loc[games_df.HOME_TEAM_ID != games_df.TEAM_ID_home, :]) == 0
assert len(games_df.loc[games_df.VISITOR_TEAM_ID != games_df.TEAM_ID_away, :]) == 0
games_df.drop(labels=['TEAM_ID_home', "TEAM_ID_away"], axis=1, inplace=True)
games_df.columns = [str.lower(x) for x in list(games_df.columns)]


# Drop 2019-20 and 2020-21 seasons
drop_games_idx = games_df.loc[games_df.season.isin([2019, 2020]), :].index
games_df.drop(drop_games_idx, inplace=True)

# Set datetime column
games_df.game_date_est = pd.to_datetime(games_df.game_date_est)

# Drop Preseason Games
start_dates['season_yr_start'] = start_dates['season_yr']-1
season_groups = games_df.groupby('season')
seasons = list(pd.unique(start_dates.loc[:, 'season_yr_start']))
for season in seasons:
    start_date = str(start_dates.loc[start_dates.season_yr_start == season, "start_date"].iloc[0])
    start_date = datetime.strptime(start_date, "%m/%d/%Y")
    end_date = str(start_dates.loc[start_dates.season_yr_start == season, "end_date"].iloc[0])
    end_date = datetime.strptime(end_date, "%m/%d/%Y")
    filter = season_groups.get_group(season)['game_date_est'].transform(lambda x: x < start_date or x > end_date)
    filter_idx = filter.loc[filter==True].index
    games_df = games_df.drop(filter_idx)
    print(len(games_df))

# This shows the number of games by season. We should have 1230 games. 2003=1189, 2006=1256, 2011 = 990, 2012 =1229
# 2011 was a shortened lockout season. 2012 had a game cancelled due to the Boston marathon bombing.
# I was not able to find the issue with the 2006 season. Scratch/duplicate_check.py has more info
season_groups = games_df.groupby('season').agg(len)

## Teams subset
teams_df = teams[["TEAM_ID", "ABBREVIATION"]]
teams_df.columns = ['team_id', 'abbreviation']

## Game Details subset
# min conflicts with a built-in DF method; rename to minutes
game_details.rename({'MIN': "minutes"}, axis=1, inplace=True)
game_details.columns = [str.lower(x) for x in list(game_details.columns)]
game_details.drop(labels=['plus_minus', "team_city", 'start_position'], axis=1, inplace=True)
stat_cols = ["minutes", "fgm", 'fga', 'fg_pct', 'fg3m', 'fg3a', 'fg3_pct', 'ftm', 'fta', 'ft_pct', 'oreb', 'dreb',
             'reb', 'ast', 'stl', 'blk', 'to', 'pf', 'pts']

# Indicator of rather a player played in a game
game_details['played'] = False
game_details.loc[game_details.comment.isna(), 'played'] = True

# ToDo: These columns are indicators of the cause of a player not playing. Perhaps a little overboard for this project
# but something to keep in mind for the future
# game_details['dnp_cd'] = False
# game_details['injured'] = False

# These game's reflect where it was the coach's choice for the player not to play. These players were, in theory,
# healthy and available for these games. Therefore, we set their 'played' variable to True and their stats to 0
game_details.loc[(game_details.comment == "DNP - Coach's Decision"), stat_cols] = 0
game_details.loc[(game_details.comment == "DNP - Coach's Decision"), 'played'] = True


# Join Tables
player_df = games_df.merge(game_details, left_on="game_id", right_on='game_id', suffixes=("_x", "_y"), how="inner")
player_df = player_df.sort_values(by="game_date_est")

# Coerce minutes to floats
minutes = player_df.minutes
minutes = minutes.str.split(":", expand=True)
minutes.columns = ['mins', 'secs']
minutes.loc[minutes.mins.isna(), 'mins'] = 0
minutes.loc[minutes.secs.isna(), 'secs'] = 0
minutes.mins = minutes.mins.astype('float')
minutes.secs = minutes.secs.astype('float')
minutes['total'] = minutes.mins + (1/60) * minutes.secs
player_df.minutes = minutes['total']

# Add Columns for rolling avg_stats
avg_stat_cols = [x+'_avg' for x in stat_cols]
null_series = pd.Series([None for _ in range(len(player_df))])
avg_stat_empty_series = {col: null_series for col in avg_stat_cols}
player_df.assign(**avg_stat_empty_series)

# 1. Group By Player
player_groups = player_df.groupby('player_id')

for key in list(player_groups.groups.keys()):
    df = player_groups.get_group(key)
    player_df.loc[df.index, avg_stat_cols] = df.loc[:, stat_cols].rolling(82, 0).mean().reindex_like(df).loc[:,
                                    stat_cols].values

ma_cols = ['game_date_est', 'game_id', 'home_team_id', 'visitor_team_id', 'season',
       'team_id', 'team_abbreviation', 'player_id', 'player_name', 'comment', 'played'] + avg_stat_cols

moving_avg_player_df = player_df.loc[:, ma_cols]
moving_avg_player_df.to_csv("./data/moving_avg_player_stats.csv")
