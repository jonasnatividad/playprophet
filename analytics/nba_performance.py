import csv

# Initialize counters for moneyline results
moneyline_total_games = 0
moneyline_win_count = 0

# Initialize counters for over/under results
o_u_total_games = 0
o_u_win_count = 0

# Open and read the CSV file
with open('analytics/nba_analyzer.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Iterate through each row in the CSV
    for row in csv_reader:
        moneyline_result = row['moneyline_result']
        o_u_result = row['o_u_result']

        # Update moneyline counters
        moneyline_total_games += 1
        if moneyline_result == 'Win':
            moneyline_win_count += 1

        # Update over/under counters
        o_u_total_games += 1
        if o_u_result == 'Win':
            o_u_win_count += 1

# Calculate win percentages as decimals
moneyline_win_ratio = moneyline_win_count / moneyline_total_games
o_u_win_ratio = o_u_win_count / o_u_total_games

# Create a new CSV file to store the win ratios as decimals
with open('web_app/nba_performance.csv', mode='w', newline='') as csv_file:
    fieldnames = ['O/U Win Ratio', 'ML Win Ratio']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'O/U Win Ratio': f'{o_u_win_ratio:.4f}', 'ML Win Ratio': f'{moneyline_win_ratio:.4f}'})

print("Win ratios as decimals have been written to nba_performance.csv.")
