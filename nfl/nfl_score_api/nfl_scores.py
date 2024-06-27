import requests
import csv
from datetime import datetime

def get_current_nfl_week():
    # Define the start date of the NFL season and the current date
    nfl_start_date = datetime(2023, 9, 7)  # Replace with the actual start date of the NFL season
    current_date = datetime.now()

    # Calculate the week number based on the current date
    delta = current_date - nfl_start_date
    current_week = 1 + delta.days // 7

    return current_week

def modify_team_name(team_name):
    if team_name == "Los Angeles Chargers":
        return "LA Chargers"
    elif team_name == "Los Angeles Rams":
        return "LA Rams"
    elif team_name == "New York Jets":
        return "NY Jets"
    elif team_name == "New York Giants":
        return "NY Giants"
    else:
        # Split the team name by space and take all words except the last one
        words = team_name.split()
        if len(words) > 1:
            return ' '.join(words[:-1])
        else:
            return team_name

def get_nfl_scores_to_csv():
    # Get the current NFL week
    week_number = get_current_nfl_week()

    # Define the API URL for the NFL scoreboard
    api_url = f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?week={week_number}'

    try:
        # Send an HTTP GET request to the API URL
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Create a CSV file and write headers
            with open('nfl/nfl_score_api/nfl_scores.csv', mode='w', newline='') as csv_file:
                fieldnames = ['team_1_name', 'team_1_actual_points', 'team_2_name', 'team_2_actual_points']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                # Extract and write the games and scores to the CSV file
                for event in data['events']:
                    home_team = modify_team_name(event['competitions'][0]['competitors'][0]['team']['displayName'])  # Switched
                    home_score = event['competitions'][0]['competitors'][0]['score']  # Switched
                    away_team = modify_team_name(event['competitions'][0]['competitors'][1]['team']['displayName'])  # Switched
                    away_score = event['competitions'][0]['competitors'][1]['score']  # Switched

                    writer.writerow({
                        'team_1_name': away_team,
                        'team_1_actual_points': away_score,
                        'team_2_name': home_team,
                        'team_2_actual_points': home_score
                    })

                print("Data has been saved to nfl_scores.csv")

        else:
            print(f"Failed to retrieve NFL scores for week {week_number}. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    get_nfl_scores_to_csv()
