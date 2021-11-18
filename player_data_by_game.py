import pandas as pd
import numpy as np

games = pd.read_csv("./data/nba_games_data/games.csv")
game_details = pd.read_csv("./data/nba_games_data/games_details.csv")
teams = pd.read_csv("./data/nba_games_data/teams.csv")

# Subset tables to only include relevant columns
## Games subset
games_df = games[["GAME_DATE_EST", "GAME_ID", "HOME_TEAM_ID", "TEAM_ID_home", "VISITOR_TEAM_ID", "TEAM_ID_away", "SEASON"]]
# Ensure the two id columns are equivalent
assert len(games_df.loc[games_df.HOME_TEAM_ID != games_df.TEAM_ID_home]) == 0
assert len(games_df.loc[games_df.VISITOR_TEAM_ID != games_df.TEAM_ID_away]) == 0
games_df.drop(labels=['TEAM_ID_home', "TEAM_ID_away"], axis=1, inplace=True)
games_df.columns = ['game_date', 'game_id', 'home_id', 'away_id']

## Teams subset
teams_df = teams[["TEAM_ID", "ABBREVIATION"]]
teams_df.columns = ['team_id', 'abbreviation']

## Game Details subset
game_details.columns = [str.lower(x) for x in list(game_details.columns)]
game_details.drop(labels=['plus_minus', "team_city"], axis=1, inplace=True)

# Data Validation - There's a set of unmatched game_ids present in the games table but not game_details. These appear
# to be preseason games from the 2003 season and lack data. We run a few checks here to make sure
unique_gd = list(pd.unique(game_details.game_id))
unique_g = list(pd.unique(games_df.game_id))
unmatched_id = [i for i in unique_g if i not in unique_gd]
unmatched_games = games.loc[games.GAME_ID.isin(unmatched_id), :]
# Assert that all games are 2003
assert (unmatched_games.GAME_DATE_EST.str[0:4] == '2003').all()
# Assert that all of a statistic is NA
assert unmatched_games.REB_away.isna().all()

# Join Tables
player_df = game_details.merge(games_df, left_on="game_id", right_on='game_id', suffixes=("_x", "_y"), how="outer")

