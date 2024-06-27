from dotenv import load_dotenv
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import tweepy

#Load environment variables from .env file
load_dotenv()

# Dictionary mapping full city names to 3-letter codes
city_codes = {
    'Arizona': 'ARI',
    'Atlanta': 'ATL',
    'Baltimore': 'BAL',
    'Buffalo': 'BUF',
    'Carolina': 'CAR',
    'Chicago': 'CHI',
    'Cincinnati': 'CIN',
    'Cleveland': 'CLE',
    'Dallas': 'DAL',
    'Denver': 'DEN',
    'Detroit': 'DET',
    'Green Bay': 'GB',
    'Houston': 'HOU',
    'Indianapolis': 'IND',
    'Jacksonville': 'JAX',
    'Kansas City': 'KC',
    'Las Vegas': 'LV',
    'LA Chargers': 'LAC',
    'LA Rams': 'LAR',
    'Miami': 'MIA',
    'Minnesota': 'MIN',
    'New England': 'NE',
    'New Orleans': 'NO',
    'NY Giants': 'NYG',
    'NY Jets': 'NYJ',
    'Philadelphia': 'PHI',
    'Pittsburgh': 'PIT',
    'San Francisco': 'SF',
    'Seattle': 'SEA',
    'Tampa Bay': 'TB',
    'Tennessee': 'TEN',
    'Washington': 'WAS',
}

# Read the CSV file into a DataFrame
csv_file_path = 'web_app/nfl_monte_carlo.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file_path)

# Mapping function to replace team names with 3-letter codes
def map_team_names(team_name):
    return city_codes.get(team_name, team_name)

# Apply the mapping function to the relevant columns
df['team_name_1'] = df['team_name_1'].apply(map_team_names)
df['team_name_2'] = df['team_name_2'].apply(map_team_names)

# Select and rearrange specific columns
selected_columns = ['team_name_1', 'team_1_win_percentage', 'team_name_2', 'team_2_win_percentage', 'total_adj_points']
df_selected = df[selected_columns]

# Rename columns
df_selected.columns = ['Away', 'Win %', 'Home', 'Win %', 'Total Points']

# Round numerical values to two decimal places
df_selected['Win %'] = (df_selected['Win %'] * 100).round(2).astype(str) + '%'
df_selected.loc[:, 'Total Points'] = df_selected['Total Points'].round(2)

# Set up Seaborn style
sns.set(style="darkgrid", rc={"axes.facecolor": "#4B0082"})

# Create a figure and axis with recommended dimensions for Twitter images
fig, ax = plt.subplots(figsize=(1200/80, 675/80))  # Adjust the figsize as needed (dividing by 80 for demonstration purposes)

# Set the background color of the entire figure
fig.patch.set_facecolor('#CCCCCC')  # Light gray color

# Hide the axes
ax.axis('off')

# Create a table using pandas.plotting.table
table = pd.plotting.table(ax, df_selected, loc='center', colWidths=[0.25] * len(df_selected.columns), cellLoc='center')  # Adjust the width as needed

# Adjust the cell heights
for key, cell in table.get_celld().items():
    if key[0] == 0:
        cell.set_text_props(fontsize=34, color='white', weight='bold', style='italic', fontfamily='Arial')
        cell.set_height(0.2)  # Adjust the row height as needed
        cell.set_edgecolor('white')
        cell.set_facecolor('#2c2a5a' if key[0] % 2 == 0 else '#393680')  # Deep purple for even rows, lighter purplish-blue for odd rows
    else:
        cell.set_text_props(fontsize=30, color='white', fontfamily='Arial')
        cell.set_height(0.1)  # Adjust the row height as needed
        cell.set_edgecolor('white')
        cell.set_facecolor('#2c2a5a' if key[0] % 2 == 0 else '#393680')  # Deep purple for even rows, lighter purplish-blue for odd rows

# Save the figure as an image without white space
plt.savefig('social/nfl_tweet.png', bbox_inches='tight', pad_inches=0, dpi=104)

api_key = os.environ.get("X_API_KEY")
api_secret = os.environ.get("X_API_SECRET_KEY")
bearer_token = os.environ.get("X_BEARER_TOKEN")
access_token = os.environ.get("X_ACCESS_TOKEN")
access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Replace the previous image_path with the newly saved image path
image_path = 'social/nfl_tweet.png'  # Replace with the path to your image file

# Upload the image without additional owners
media = api.media_upload(filename=image_path)

# Get the media ID from the response
media_id = media.media_id

# Text content of the tweet
main_text = "Weekly 🏈 Predictions\n Powered by www.playprophet.ai 🔮"
hashtags = "#SportsBetting #PlayProphet #NFLBetting #NFLPredictions #NFLGambling #NFLResults #GamblingTwitter #NFL"  
tweet_content = main_text + "\n\n" + hashtags

# Post the tweet with the image
client.create_tweet(text=tweet_content, media_ids=[media_id])