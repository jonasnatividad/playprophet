import requests
import csv
from datetime import datetime, timedelta

def modify_team_name(team_name):
    if team_name == "Los Angeles Lakers":
        return "LA Lakers"
    elif team_name == "Los Angeles Clippers":
        return "LA Clippers"
    elif team_name == "Portland Trail Blazers":
        return "Portland"
    elif team_name == "Oklahoma City Thunder":
        return "Okla City"
    else:
        # Split the team name by space and take all words except the last one
        words = team_name.split()
        if len(words) > 1:
            return ' '.join(words[:-1])
        else:
            return team_name

def get_nba_scores_to_csv(date):
    # Define the API URL for the NBA scoreboard
    api_url = f'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?date={date}'

    try:
        # Send an HTTP GET request to the API URL
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Create a CSV file and write headers
            with open('nba/nba_score_api/nba_scores.csv', mode='w', newline='') as csv_file:
                fieldnames = ['team_1_name', 'team_1_actual_points', 'team_2_name', 'team_2_actual_points']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                # Extract and write the games and scores to the CSV file with home and away teams switched
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

                print("Data has been saved to nba_scores.csv")

        else:
            print(f"Failed to retrieve NBA scores. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    yesterday = datetime.now() - timedelta(1)
    date = yesterday.strftime('%Y-%m-%d')
    get_nba_scores_to_csv(date)
