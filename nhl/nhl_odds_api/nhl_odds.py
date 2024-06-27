from dotenv import load_dotenv
import os
import pandas as pd
import requests

#Load environment variables from .env file
load_dotenv()

# Set the sport to 'basketball_nhl' for nhl games
SPORT = 'icehockey_nhl'

# Set regions to 'us' for United States
REGIONS = 'us'

# Set markets to 'totals' to get over/under odds
MARKETS = 'totals'

# Set odds format to 'american' if needed
ODDS_FORMAT = 'american'

# Set date format to 'iso' if needed
DATE_FORMAT = 'iso'

# Set the bookmaker to 'draftkings' to filter by DraftKings
BOOKMAKER = 'draftkings'

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

# Create empty lists to store data
team1_list = []
team2_list = []
point_value_list = []

# Make a request to get odds for NHL over/under markets
odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    params={
        'api_key': os.environ.get("ODDS_API_KEY"),
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
else:
    odds_json = odds_response.json()

    # Iterate through the events to get the over/under lines for each event
    for event in odds_json:
        team1 = event['home_team']
        team2 = event['away_team']
        point_value = None

        for bookmaker in event['bookmakers']:
            if bookmaker['key'] == BOOKMAKER:
                for market in bookmaker['markets']:
                    if market['key'] == 'totals':
                        for outcome in market['outcomes']:
                            if outcome['name'] == 'Over':
                                point_value = outcome['point']

        if point_value is not None:
            # Modify team names using the function
            team1 = modify_team_name(team1)
            team2 = modify_team_name(team2)

            team1_list.append(team1)
            team2_list.append(team2)
            point_value_list.append(point_value)

    # Create a DataFrame
    data = {
        'team_1_name': team2_list,
        'team_2_name': team1_list,
        'total_o_u_points': point_value_list,
    }

    df = pd.DataFrame(data)

    # Export the DataFrame to a CSV file
    df.to_csv('nhl/nhl_odds_api/nhl_odds.csv', index=False)

    # Print the DataFrame (optional)
    print(df)
