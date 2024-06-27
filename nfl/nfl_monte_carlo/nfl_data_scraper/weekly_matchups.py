#!/usr/bin/env python3
import csv
from dotenv import load_dotenv
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Load environment variables from .env file
load_dotenv()

url = os.environ.get("NFL_WM_URL")

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


# Wait for the table to load
driver.implicitly_wait(10)

# Find the table element by its ID
table_body = driver.find_element(By.ID, 'DataTables_Table_0')

# Initialize an empty list to store the teams
teams = []

# Regular expression pattern to match "@" and "vs."
pattern = re.compile(r'@|vs\.')

# Initialize an empty list to store team pairs
team_pairs = []

# Iterate through each row in the table
for row in table_body.find_elements(By.XPATH, '//tbody/tr'):
    # Find the team name within the first column of the row
    team_name = row.find_element(By.XPATH, './td[1]/a').text
    # Split the team names using the regular expression pattern
    team_names_split = pattern.split(team_name)
    # Append both teams to the list
    teams.extend(team_names_split)

    # If we have processed two teams, add them to the team_pairs list and reset the teams list
    if len(teams) == 2:
        team_pairs.append(teams)
        teams = []

# Close the WebDriver
driver.quit()

# Define the full path to the output file
output_file_path = 'nfl/nfl_monte_carlo/nfl_data_scraper/weekly_matchups.csv'

# Add header names
header = ['team_name_1', 'team_name_2']

# Write the pairs of teams to a CSV file with headers
with open(output_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)  # Write the header
    for pair in team_pairs:
        csv_writer.writerow(pair)
