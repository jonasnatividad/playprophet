import csv
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

#Load environment variables from .env file
load_dotenv()

# Function to modify team names
def modify_team_name(team_name):
    if team_name == "Detroit Red Wings":
        return "Detroit"
    elif team_name == "Tampa Bay":
        return "Tampa Bay"
    elif team_name == "Toronto Maple Leafs":
        return "Toronto"
    elif team_name == "Columbus Blue Jackets":
        return "Columbus"
    elif team_name == "New Jersey":
        return "New Jersey"
    elif team_name == "NY Islanders":
        return "NY Islanders"
    elif team_name == "NY Rangers":
        return "NY Rangers"
    elif team_name == "St. Louis":
        return 'St. Louis'
    elif team_name == "Los Angeles":
        return "LA Kings"
    elif team_name == "San Jose":
        return "San Jose"
    elif team_name == "Vegas":
        return "Las Vegas"
    elif team_name == "Montréal Canadiens":
        return "Montreal"
    else:
        # Split the team name by space and take all words except the last one
        words = team_name.split()
        if len(words) > 1:
            return ' '.join(words[:-1])
        else:
            return team_name

url = os.environ.get("NHL_PA_URL")

# Set up the Chrome WebDriver with additional options for headless mode
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--disable-infobars')
options.add_argument('--mute-audio')

driver = webdriver.Chrome(options=options)
driver.get(url)

try:
    # Wait for the table to be present in the DOM
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table.graph-table'))
    )

    # Extract and print the headers
    headers = [th.text.strip() for th in table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')]

    # Find the index of 'GA/G' in the headers
    ga_per_game_index = headers.index('GA/G')

    # Get the current timestamp
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Extract and write the data to a CSV file
    with open(f'nhl/nhl_monte_carlo/nhl_data_scraper/points_allowed.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write headers to the CSV file with the renamed column
        csv_writer.writerow(['team', 'pa_2023', 'timestamp'])

        # Extract and write the data for the 'Team' and 'GA/G' columns
        for row in table.find_elements(By.TAG_NAME, 'tbody')[0].find_elements(By.TAG_NAME, 'tr'):
            columns = row.find_elements(By.TAG_NAME, 'td')
            team_name = columns[0].text.strip()  # Assuming 'Team' is the first column
            ga_per_game = columns[ga_per_game_index].text.strip()

            # Modify team names using the function
            team_name = modify_team_name(team_name)

            # Write the row to the CSV file with the timestamp
            csv_writer.writerow([team_name, ga_per_game, current_timestamp])

finally:
    # Close the browser window
    driver.quit()
