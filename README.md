# W207_Final_NBA_Prediction
W207 Final project for predicting NBA games 

The `submission` folder contains most of the main files used to generate our final models and report. 

Several scripts that were important to the project are left out of the submission folder because moving them to submission would break their functionality. These scripts are: 
- `cluster_assignment.py` - clusters players and writes out the data to `cluster_by_player.csv` and `cluster_by_team.csv`
- `player_data_by_game.py` - computes players' rolling average statistics used for clustering and writes the data to `moving_avg_player_stats.csv`. 
This file is too large to be stored in git, and this script will need to be run to execute the project locally. 

The following files were part of our initial data exploration, proofs of concept, or used to practice model building. These files are ancillary and not needed to understand the project:
- `DEA_NBA_Baseline.ipynb`
- `Data Explore NBA.ipynb`
- `clustering_MK.ipynb`
- `example_data_frame.ipynb`
- `hyperparameter_tuning_practice.ipynb`
- `neural_network_practice.ipynb`
- `player_cluster.ipynb`
- `player_stats.ipynb`
- `supervised_training.ipynb` 
