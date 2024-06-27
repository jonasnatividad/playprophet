#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import os

# Specify the name of the folder within your working directory
folder_name = 'nba/nba_monte_carlo/nba_data_scraper'  # Change this to the desired folder name

# Create the full path to the folder
folder_path = os.path.join(os.getcwd(), folder_name)

# Check if the folder exists, and create it if it doesn't
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# URL of the webpage to scrape
url = "https://www.teamrankings.com/nba/schedules/"

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

# Wait for the "Accept Cookies" button to be present and click it
try:
    accept_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Accept All Cookies']"))
    )
    accept_button.click()
except Exception as e:
    print("Could not click the 'Accept All Cookies' button:", str(e))

# Wait for tables to load
driver.implicitly_wait(10)

# Find the table element by its class name
table = driver.find_element(By.CLASS_NAME, 'tr-table')

# Check if the table exists
if table:
    # Initialize a list to store data
    data = []

    # Find all table rows using Selenium
    rows = table.find_elements(By.TAG_NAME, 'tr')

    for row in rows[1:]:  # Skip the header row
        # Extract data from each row
        cells = row.find_elements(By.TAG_NAME, 'td')

        if len(cells) >= 3:
            matchup = cells[2].text.strip()
            
            # Split the "Matchup" field into team names by " at "
            team_names = matchup.split(' at ')

            if len(team_names) == 2:
                team_name_1, team_name_2 = team_names
            else:
                team_name_1, team_name_2 = '', ''

            # Remove leading and trailing whitespace while preserving spaces between words
            team_name_1 = team_name_1.strip()
            team_name_2 = team_name_2.strip()

            # Use regular expressions to remove numbers and "#" symbols
            team_name_1 = re.sub(r'[^a-zA-Z\s]', '', team_name_1)
            team_name_2 = re.sub(r'[^a-zA-Z\s]', '', team_name_2)

            # Remove extra spaces between words
            team_name_1 = ' '.join(team_name_1.split())
            team_name_2 = ' '.join(team_name_2.split())

            # Store the data in a list
            data.append([team_name_1, team_name_2])

    # Define the CSV file name
    csv_filename = 'daily_matchups.csv'

    # Specify the CSV file path within the specified folder
    csv_file = os.path.join(folder_path, csv_filename)

    # Write the data to a CSV file at the specified location
    with open(csv_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write the header row
        csv_writer.writerow(['team_name_1', 'team_name_2'])
        # Write the data rows
        csv_writer.writerows(data)

else:
    print("Table with the specified class not found.")

# Close the Selenium WebDriver
driver.quit()
