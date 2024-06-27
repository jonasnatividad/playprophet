#!/usr/bin/env python3
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

# Specify the name of the folder within your working directory
folder_name = 'nba/nba_monte_carlo/nba_data_scraper'  # Change this to the desired folder name

# Create the full path to the folder
folder_path = os.path.join(os.getcwd(), folder_name)

# Check if the folder exists, and create it if it doesn't
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Specify the URL of the N data page
url = os.environ.get("NBA_PF_URL")

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

# Find the table element
table = driver.find_element(By.ID, "DataTables_Table_0")

# Find all rows within the table
rows = table.find_elements(By.TAG_NAME, "tr")

# Specify the CSV file path
csv_file = os.path.join(folder_path, 'points_forced.csv')

with open(csv_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['ranking', 'team', 'pf_2023', 'last_3', 'last_1', 'home', 'away', 'pf_2022', 'pf_average', 'timestamp'])  # Add more column headers as needed

    # Loop through the rows and extract data
    for row in rows[1:]:  # Skip the header row
        # Extract data from each column in the row
        columns = row.find_elements(By.TAG_NAME, "td")

        # Access specific data elements by index (e.g., columns[0] for the first column)
        rank = columns[0].text
        team_name = columns[1].text
        pf_2023 = columns[2].text
        pf_2022 = columns[7].text

        # Calculate the pa_average field
        if not pf_2023.strip().replace(".", "").isdigit():
            pf_average = float(pf_2022)
        else:
            pf_average = (float(pf_2023) + float(pf_2022)) / 2

        # Format pf_average with 2 decimal places
        formatted_pf_average = "{:.2f}".format(pf_average)

        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Write data to CSV file
        csv_writer.writerow([rank, team_name, pf_2023, columns[3].text, columns[4].text, columns[5].text, columns[6].text, pf_2022, formatted_pf_average, timestamp])

# Quit the Chrome WebDriver
driver.quit()
