import requests
import csv
from datetime import datetime, timedelta

# Function to modify team names
def modify_team_name(team_name):
    if team_name == "Detroit Red Wings":
        return "Detroit"
    elif team_name == "Tampa Bay Lightning":
        return "Tampa Bay"
    elif team_name == "Toronto Maple Leafs":
        return "Toronto"
    elif team_name == "Columbus Blue Jackets":
        return "Columbus"
    elif team_name == "New Jersey Devils":
        return "New Jersey"
    elif team_name == "New York Islanders":
        return "NY Islanders"
    elif team_name == "New York Rangers":
        return "NY Rangers"
    elif team_name == "St. Louis Blues":
        return "St. Louis"
    elif team_name == "Los Angeles Kings":
        return "LA Kings"
    elif team_name == "San Jose Sharks":
        return "San Jose"
    elif team_name == "Vegas Golden Knights":
        return "Las Vegas"
    else:
        # Split the team name by space and take all words except the last one
        words = team_name.split()
        if len(words) > 1:
            return ' '.join(words[:-1])
        else:
            return team_name

def get_nhl_scores_to_csv(date):
    # Define the API URL for the NHL scoreboard
    api_url = f'https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard?date={date}'

    try:
        # Send an HTTP GET request to the API URL
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Create a CSV file and write headers
            with open('nhl/nhl_score_api/nhl_scores.csv', mode='w', newline='') as csv_file:
                fieldnames = ['team_1_name', 'team_1_actual_points', 'team_2_name', 'team_2_actual_points']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                # Extract and write the games and scores to the CSV file
                for event in data['events']:
                    home_team = modify_team_name(event['competitions'][0]['competitors'][0]['team']['displayName'])
                    home_score = event['competitions'][0]['competitors'][0]['score']
                    away_team = modify_team_name(event['competitions'][0]['competitors'][1]['team']['displayName'])
                    away_score = event['competitions'][0]['competitors'][1]['score']

                    writer.writerow({
                        'team_1_name': away_team,
                        'team_1_actual_points': away_score,
                        'team_2_name': home_team,
                        'team_2_actual_points': home_score
                    })

                print("Data has been saved to nhl_scores.csv")

        else:
            print(f"Failed to retrieve NHL scores. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    yesterday = datetime.now() - timedelta(1)
    date = yesterday.strftime('%Y-%m-%d')
    get_nhl_scores_to_csv(date)
