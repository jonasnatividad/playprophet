from dotenv import load_dotenv
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import tweepy

#Load environment variables from .env file
load_dotenv()

city_codes = {
    'Anaheim': 'ANA',
    'Arizona': 'ARI',
    'Boston': 'BOS',
    'Buffalo': 'BUF',
    'Calgary': 'CGY',
    'Carolina': 'CAR',
    'Chicago': 'CHI',
    'Colorado': 'COL',
    'Columbus': 'CBJ',
    'Dallas': 'DAL',
    'Detroit': 'DET',
    'Edmonton': 'EDM',
    'Florida': 'FLA',
    'LA Kings': 'LAK',
    'Minnesota': 'MIN',
    'Montreal': 'MTL',
    'Nashville': 'NSH',
    'New Jersey': 'NJD',
    'NY Islanders': 'NYI',
    'NY Rangers': 'NYR',
    'Ottawa': 'OTT',
    'Philadelphia': 'PHI',
    'Pittsburgh': 'PIT',
    'San Jose': 'SJS',
    'Seattle': 'SEA',
    'St. Louis': 'STL',
    'Tampa Bay': 'TBL',
    'Toronto': 'TOR',
    'Vancouver': 'VAN',
    'Las Vegas': 'VGK',
    'Washington': 'WSH',
    'Winnipeg': 'WPG',
}

csv_file_path = 'web_app/nhl_monte_carlo.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file_path)

def map_team_names(team_name):
    return city_codes.get(team_name, team_name)

df['team_name_1'] = df['team_name_1'].apply(map_team_names)
df['team_name_2'] = df['team_name_2'].apply(map_team_names)

selected_columns = ['team_name_1', 'team_1_win_percentage', 'team_name_2', 'team_2_win_percentage', 'total_adj_points']
df_selected = df[selected_columns]

df_selected.columns = ['Away', 'Win %', 'Home', 'Win %', 'Total Points']

df_selected['Win %'] = (df_selected['Win %'] * 100).round(2).astype(str) + '%'
df_selected.loc[:, 'Total Points'] = df_selected['Total Points'].round(2)

# Check for 'nan' text in the DataFrame
contains_nan_text = df_selected.applymap(lambda x: 'nan' in str(x)).any().any()

if not contains_nan_text:
    sns.set(style="darkgrid", rc={"axes.facecolor": "#4B0082"})

    fig, ax = plt.subplots(figsize=(1200/80, 675/80))
    fig.patch.set_facecolor('#CCCCCC')
    ax.axis('off')

    table = pd.plotting.table(ax, df_selected, loc='center', colWidths=[0.25] * len(df_selected.columns), cellLoc='center')

    for key, cell in table.get_celld().items():
        if key[0] == 0:
            cell.set_text_props(fontsize=34, color='white', weight='bold', style='italic', fontfamily='Arial')
            cell.set_height(0.2)
            cell.set_edgecolor('white')
            cell.set_facecolor('#2c2a5a' if key[0] % 2 == 0 else '#393680')
        else:
            cell.set_text_props(fontsize=30, color='white', fontfamily='Arial')
            cell.set_height(0.1)
            cell.set_edgecolor('white')
            cell.set_facecolor('#2c2a5a' if key[0] % 2 == 0 else '#393680')

    plt.savefig('social/nhl_tweet.png', bbox_inches='tight', pad_inches=0, dpi=104)

    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET_KEY")
    bearer_token = os.environ.get("X_BEARER_TOKEN")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    image_path = 'social/nhl_tweet.png'
    media = api.media_upload(filename=image_path)
    media_id = media.media_id

    main_text = "Daily 🏒 Predictions\n Powered by www.playprophet.ai 🔮"
    hashtags = "#SportsBetting #PlayProphet #NHLBetting #NHLPredictions #NHLGambling #NHLResults #GamblingTwitter #NHL"  
    tweet_content = main_text + "\n\n" + hashtags

    client.create_tweet(text=tweet_content, media_ids=[media_id])
else:
    print("DataFrame contains 'nan'. Tweet will not be posted.")
