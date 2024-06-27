#!/usr/bin/env python3

import pandas as pd
import numpy as np
from scipy.stats import norm
import os

# Read the data from CSV files in their respective folders
daily_matchups = 'nhl/nhl_monte_carlo/nhl_data_scraper/daily_matchups.csv'
pf_csv = 'nhl/nhl_monte_carlo/nhl_data_scraper/points_forced.csv'
pa_csv = 'nhl/nhl_monte_carlo/nhl_data_scraper/points_allowed.csv'

Daily_Matchups = pd.read_csv(daily_matchups)
pf_df = pd.read_csv(pf_csv)
pa_df = pd.read_csv(pa_csv)

# Strip leading and trailing whitespace from team names
Daily_Matchups['team_name_1'] = Daily_Matchups['team_name_1'].str.strip()
Daily_Matchups['team_name_2'] = Daily_Matchups['team_name_2'].str.strip()
pf_df['team'] = pf_df['team'].str.strip()
pa_df['team'] = pa_df['team'].str.strip()

# Merge the DataFrames on 'team_name_1' and 'team_name_2'
merged_df = Daily_Matchups.merge(pf_df, left_on='team_name_1', right_on='team', how='left')
merged_df = merged_df.rename(columns={'pf_2023': 'team_1_pf'})

# Merge again for the second team (team_name_2)
merged_df = merged_df.merge(pf_df, left_on='team_name_2', right_on='team', how='left')
merged_df = merged_df.rename(columns={'pf_2023': 'team_2_pf'})

# Merge again for the second team (team_name_2)
merged_df = merged_df.merge(pa_df, left_on='team_name_1', right_on='team', how='left', suffixes=('_team_1', '_team_2'))
merged_df = merged_df.rename(columns={'pa_2023_team_1': 'team_1_pa', 'pa_2023_team_2': 'team_2_pa'})

# Merge again for the second team (team_name_2)
merged_df = merged_df.merge(pa_df, left_on='team_name_2', right_on='team', how='left', suffixes=('_team_1', '_team_2'))
merged_df = merged_df.rename(columns={'pa_2023_team_1': 'team_1_pa', 'pa_2023_team_2': 'team_2_pa'})

# Add timestamp fields from total_pf and total_pa
merged_df['team_1_pf_timestamp'] = pf_df['timestamp']
merged_df['team_2_pf_timestamp'] = pf_df['timestamp']
merged_df['team_1_pa_timestamp'] = pa_df['timestamp']
merged_df['team_2_pa_timestamp'] = pa_df['timestamp']

# Drop the redundant columns and reorder them
merged_df = merged_df[['team_name_1', 'team_1_pf', 'team_1_pf_timestamp', 'team_1_pa', 'team_1_pa_timestamp', 'team_name_2', 'team_2_pf', 'team_2_pf_timestamp', 'team_2_pa', 'team_2_pa_timestamp']]

# Calculate Team 1 Adjusted Points and Append to Table
merged_df['team_1_adj_pts'] = np.sqrt(merged_df['team_1_pf'] * merged_df['team_2_pa'])

# Calculate Team 2 Adjusted Points and Append to Table
merged_df['team_2_adj_pts'] = np.sqrt(merged_df['team_1_pa'] * merged_df['team_2_pf'])

# Add a field for total adjusted points (sum of team_1_adj_pts and team_2_adj_pts)
merged_df['total_adj_points'] = merged_df['team_1_adj_pts'] + merged_df['team_2_adj_pts']

# Number of Monte Carlo simulations
num_simulations = 1000000

# Initialize win counts for both teams
team_1_wins = np.zeros(len(merged_df))
team_2_wins = np.zeros(len(merged_df))

# Iterate through simulations for each matchup
for i in range(len(merged_df)):
    team_1_adj_pts = merged_df.loc[i, 'team_1_adj_pts']
    team_2_adj_pts = merged_df.loc[i, 'team_2_adj_pts']
    
    team_1_wins_count = 0
    team_2_wins_count = 0
    
    for _ in range(num_simulations):
        # Simulate a random outcome for each team based on the normal distributions
        team_1_score = np.random.normal(team_1_adj_pts, scale=10)
        team_2_score = np.random.normal(team_2_adj_pts, scale=10)
        
        # Count wins
        if team_1_score > team_2_score:
            team_1_wins_count += 1
        elif team_2_score > team_1_score:
            team_2_wins_count += 1
    
    # Calculate win percentages for this matchup
    team_1_win_percentage = team_1_wins_count / num_simulations
    team_2_win_percentage = team_2_wins_count / num_simulations
    
    # Update the win counts for each team
    team_1_wins[i] = team_1_wins_count
    team_2_wins[i] = team_2_wins_count

# Calculate win percentages for each team based on the total number of wins
total_wins = team_1_wins + team_2_wins
team_1_win_percentages = (team_1_wins / total_wins)
team_2_win_percentages = (team_2_wins / total_wins)

# Append win percentage columns to the existing DataFrame
merged_df['team_1_win_percentage'] = team_1_win_percentages
merged_df['team_2_win_percentage'] = team_2_win_percentages

# Round all numeric values to 1 decimal place
merged_df = merged_df.round(3)

# Specify the CSV file path within the specified output folder
predictions_csv_file_path = 'web_app/nhl_monte_carlo.csv'
log_csv_file_path ='analytics/nhl_monte_carlo_log.csv'

# Save the DataFrame to a CSV file in the specified output folder
merged_df.to_csv(predictions_csv_file_path, index=False)

# Check if log file exists and is not empty, then append without header; otherwise, write with header
if os.path.isfile(log_csv_file_path) and os.path.getsize(log_csv_file_path) > 0:
    merged_df.to_csv(log_csv_file_path, mode='a', header=False, index=False)
else:
    merged_df.to_csv(log_csv_file_path, mode='w', header=True, index=False)
