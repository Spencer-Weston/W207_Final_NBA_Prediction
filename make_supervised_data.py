import numpy as np
import pandas as pd

# Import Data
cluster_data = pd.read_csv("./data/clusters_by_team.csv")
team_data = pd.read_csv("./data/game_past_data.csv")

# Clean Team Data
team_data.columns = [col.lower() for col in list(team_data.columns)]
drop_cols = ["unnamed: 0", "team_turnovers_home", "team_turnovers_away", 'game_order', 'game_reverse_order' ]
t = 2