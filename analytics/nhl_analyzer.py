import csv
import os

# Read data from nhl_monte_carlo.csv
monte_carlo_data = []
with open('web_app/nhl_monte_carlo.csv', 'r') as monte_carlo_file:
    monte_carlo_reader = csv.reader(monte_carlo_file)
    header = next(monte_carlo_reader)  # Read and skip the header
    for row in monte_carlo_reader:
        monte_carlo_data.append(row)

# Read data from nhl_scores.csv
scores_data = []
with open('nhl/nhl_score_api/nhl_scores.csv', 'r') as scores_file:
    scores_reader = csv.DictReader(scores_file)
    for row in scores_reader:
        scores_data.append(row)

# Create a dictionary to map team names to their corresponding scores data
scores_data_dict = {row['team_1_name']: row for row in scores_data}

# Update the header with the new fields
updated_header = ['team_name_1', 'team_name_2', 'timestamp', 'team_1_adj_pts', 'team_2_adj_pts', 'total_adj_pts',
                  'team_1_win_percentage', 'team_2_win_percentage', 'team_1_actual_points', 'team_2_actual_points',
                  'total_actual_points', 'moneyline_prediction', 'actual_winner', 'moneyline_result', 'total_o_u_points',
                  'o_u_prediction', 'o_u_result']

# Read data from nhl_odds.csv
odds_data = []
with open('nhl/nhl_odds_api/nhl_odds.csv', 'r') as odds_file:
    odds_reader = csv.DictReader(odds_file)
    for row in odds_reader:
        odds_data.append(row)

# Create a dictionary to map team names to their corresponding odds data
odds_data_dict = {(row['team_1_name'], row['team_2_name']): row for row in odds_data}

# Merge the data based on team names
merged_data = []
for monte_carlo_row in monte_carlo_data:
    team_name_1 = monte_carlo_row[0]
    team_1_adj_pts = float(monte_carlo_row[10])
    team_name_2 = monte_carlo_row[5]
    team_2_adj_pts = float(monte_carlo_row[11])

    scores_row = scores_data_dict.get(team_name_1)
    odds_row = odds_data_dict.get((team_name_1, team_name_2))

    if scores_row and odds_row:
        team_1_name = scores_row['team_1_name']
        team_1_actual_points = int(scores_row['team_1_actual_points'])
        team_2_name = scores_row['team_2_name']
        team_2_actual_points = int(scores_row['team_2_actual_points'])

        # Calculate the total actual points
        total_actual_points = team_1_actual_points + team_2_actual_points

        total_predicted_points = float(odds_row['total_o_u_points'])

        # Determine the prediction winner based on adjusted points
        if team_1_adj_pts > team_2_adj_pts:
            moneyline_prediction = team_name_1
        elif team_1_adj_pts < team_2_adj_pts:
            moneyline_prediction = team_name_2
        else:
            moneyline_prediction = "Tie"

        # Determine the winner based on actual points
        if team_1_actual_points > team_2_actual_points:
            actual_winner = team_1_name
        elif team_1_actual_points < team_2_actual_points:
            actual_winner = team_2_name
        else:
            actual_winner = "Tie"

        # Determine the moneyline result
        moneyline_result = "Win" if moneyline_prediction == actual_winner else "Loss"

        # Determine the over/under prediction
        if float(monte_carlo_row[12]) > total_predicted_points:
            o_u_prediction = "Over"
        elif float(monte_carlo_row[12]) < total_predicted_points:
            o_u_prediction = "Under"
        else:
            o_u_prediction = "Tie"

        # Determine the over/under result
        if total_actual_points > total_predicted_points and o_u_prediction == "Over":
            o_u_result = "Win"
        elif total_actual_points < total_predicted_points and o_u_prediction == "Over":
            o_u_result = "Loss"
        elif total_actual_points > total_predicted_points and o_u_prediction == "Under":
            o_u_result = "Loss"
        elif total_actual_points < total_predicted_points and o_u_prediction == "Under":
            o_u_result = "Win"
        else:
            o_u_result = "Tie"

        # Rename 'team_1_pa_timestamp' to 'timestamp'
        team_1_pa_timestamp = monte_carlo_row[9]

        # Prepare the data for output
        output_data = [team_name_1, team_name_2, team_1_pa_timestamp, team_1_adj_pts, team_2_adj_pts, monte_carlo_row[12],
                       monte_carlo_row[13], monte_carlo_row[14], team_1_actual_points, team_2_actual_points, 
                       total_actual_points, moneyline_prediction, actual_winner, moneyline_result, total_predicted_points,
                       o_u_prediction, o_u_result]

        merged_data.append(output_data)

# Append the merged data to the existing file "nhl_analyzer.csv" with the updated header
output_file = 'analytics/nhl_analyzer.csv'
header_exists = os.path.isfile(output_file)
with open(output_file, 'a', newline='') as analyzer_file:
    analyzer_writer = csv.writer(analyzer_file)

    if not header_exists:
        # Write the updated header only if the file is empty
        analyzer_writer.writerow(updated_header)

    # Then, write the merged data
    for row in merged_data:
        analyzer_writer.writerow(row)
