import pandas as pd
import numpy as np
from datetime import datetime

games = pd.read_csv("../data/nba_games_data/games_test.csv")
start_dates = pd.read_csv("../data/season_start.csv")
games_df = games.groupby("SEASON").get_group(2006)
games_df.columns = [str.lower(x) for x in list(games_df.columns)]
games_df.game_date_est = pd.to_datetime(games_df.game_date_est)

start_dates['season_yr_start'] = start_dates['season_yr']-1
season = 2006
start_date = str(start_dates.loc[start_dates.season_yr_start == season, "start_date"].iloc[0])
start_date = datetime.strptime(start_date, "%m/%d/%Y")
end_date = str(start_dates.loc[start_dates.season_yr_start == season, "end_date"].iloc[0])
end_date = datetime.strptime(end_date, "%m/%d/%Y")

filter = games_df['game_date_est'].transform(lambda x: x < start_date or x > end_date)
filter_idx = filter.loc[filter == True].index
games_df = games_df.drop(filter_idx)

# Check for duplicate game ids (No duplicates)
assert len(pd.unique(games_df.game_id)) == 1256
# Check for duplicate home team on date
assert not (games_df.groupby(['game_date_est', 'home_team_id']).size() > 1).any()
# Check for duplicate away team on date
assert not (games_df.groupby(['game_date_est', 'visitor_team_id']).size() > 1).any()
# Check for duplicate date and id's
assert not (games_df.groupby(['game_date_est', 'visitor_team_id', 'home_team_id']).size() > 1).any()
# Check if same team plays in multiple games
assert len(games_df.loc[games_df.home_team_id == games_df.visitor_team_id]) == 0
# Check if stats are duplicated
groups = games_df.groupby(['pts_home', 'fg_pct_home',
       'ft_pct_home', 'fg3_pct_home', 'ast_home', 'reb_home',
       'pts_away', 'fg_pct_away', 'ft_pct_away', 'fg3_pct_away', 'ast_away',
       'reb_away'])
assert(len(groups)) == 1256
# Check if home stats are duplicated
groups = games_df.groupby(['pts_home', 'fg_pct_home',
       'ft_pct_home', 'fg3_pct_home', 'ast_home', 'reb_home'])
assert(len(groups)) == 1256
# Check if away stats are duplicated
groups = games_df.groupby(['pts_away', 'fg_pct_away', 'ft_pct_away', 'fg3_pct_away', 'ast_away', 'reb_away'])
assert(len(groups)) == 1256

# Check for any duplicates with a different method
v_counts =games_df.value_counts()
assert not (v_counts > 1).any()
t = 2
