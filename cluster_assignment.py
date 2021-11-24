import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load data; Drop row number column; other data formatting
cluster_data = pd.read_csv("./data/kmeans_data.csv")
cluster_data.columns = [str.lower(x) for x in cluster_data.columns]
cluster_data = cluster_data.drop(columns=['unnamed: 0', 'reb_y', 'ast_y', 'pts_y', 'draft_flag', 'height', 'weight',
                                          'reb_x', 'player_age', 'season_exp'])
cluster_data.rename({"pts_x": "pts", 'ast_x': 'ast'}, axis=1, inplace=True)

player_data = pd.read_csv("./data/moving_avg_player_stats.csv")
player_data = player_data.drop('Unnamed: 0', axis=1)
# Remove average name of columns to give equivalent columns between datasets
new_player_cols = []
for col in list(player_data.columns):
    if col.count("_avg") >= 1:
        new_col = col.replace("_avg", "")
        new_player_cols.append(new_col)
    else:
        new_player_cols.append(col)
player_data.columns = new_player_cols
player_data.rename({"minutes": "mpg", "to": 'tov'}, axis=1, inplace=True)
player_data = player_data.loc[~player_data.fga.isna(), :]

# Columns to use in clustering
cluster_cols = ['mpg', 'fga', 'fg_pct', "fg3a", 'fg3_pct', 'fta', 'ft_pct', 'oreb', 'dreb', 'ast', 'stl', 'blk', 'tov',
                'pf', 'pts']
X_train = cluster_data.loc[:, cluster_cols]
X_assign = player_data.loc[:, cluster_cols]

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_assign_scaled = scaler.transform(X_assign)

# distortions = []
# for i in range(1, 50):
#     km_mod = KMeans(n_clusters=i, init='random', max_iter=300, n_init=10, random_state=0)
#     km_mod.fit(X_train_scaled)
# #   print(km_mod.inertia_)
#     distortions.append(km_mod.inertia_)
#
# plt.figure(figsize=(8,6))
# plt.plot(range(1, 50), distortions, 'bx-')
# plt.xlabel('number of clusters', fontsize=14)
# plt.ylabel('Distortion', fontsize=14)
# plt.title('Elbow Plot', fontsize=14)
km_mod = KMeans(n_clusters=12, init='random', max_iter=300, n_init=10, random_state=0)
km_mod.fit(X_train_scaled)
predicted_clusters = km_mod.predict(X_assign_scaled)

player_data['cluster'] = predicted_clusters
cluster_titles = [f"cluster_{i}" for i in pd.unique(player_data.cluster)]
for i, clust_num in enumerate(cluster_titles):
    player_data[cluster_titles[i]] = player_data.cluster.apply(lambda x: 1 if x == i else 0)

game_cols = ['game_id', 'team_id']
game_data = player_data.loc[:, game_cols + cluster_titles]
game_grouped_data = player_data.groupby(by=game_cols).sum()
t = 2
