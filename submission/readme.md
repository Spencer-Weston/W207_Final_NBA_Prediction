# Readme for the notebooks used on the NBA Prediction Project


## Notebooks used for data loading, wrangling and DE work:
1. player_data_load.ipynb
   - Gets player stats data from nba_api
   - Gets player attributes from sqlite
   - Join the player stats and player attributes
   - Cleans player data
   - Load to player_data.csv
2. Player cluster
3. Assign player cluster to team 
4. game_data_load_and_wrangling.ipynb
   - Gets game stats data from sqlite
   - Explores the game data
   - Cleans the game data
   - Computes the historical weighted average of the games stats
   - Join with player clusters assign to the team and game 
   - Load to nba_final_data.csv

## Notebooks used for modeling:
1. **XX.ipynb**
   - Baseline and enhanced linear regression
2. **modeling_tree.ipynb**
   - This notebook include models on:    
     - Decision trees with DecisionTreeRegressor
     - Random Forest with RandomForestRegressor
     - XG Boosting with xgb
3. **NN_model_selection.ipynb**
   - Hyperparameter tuning and model selection for neural network model
4. **NN_model_evaluation.ipynb**
   - Evaluation of neural network model
5. **player_cluster_evaluation.ipynb**
   - Evaluation of player clusters 
