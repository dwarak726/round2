import time
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv

# Initialize WebDriver
driver = webdriver.Chrome()
BASE_URL = "https://www.hackerrank.com/contests/aac-problem-solving/judge/submissions"

# Prompt user to log in
driver.get(f"{BASE_URL}/challenge")
input("Log in to HackerRank, then press Enter here...")

HEADERS = ["Problem", "Team", "ID", "Language", "Time", "Result", "Score", "Status", "During Contest"]
structured_data = []

def scrape_page(page_index):
    """Scrapes submission data from a given page index."""
    url = f"{BASE_URL}/{page_index}" if page_index > 1 else f"{BASE_URL}/challenge"
    driver.get(url)
    time.sleep(3)

    try:
        # Check if there are no submissions
        if "There are no submissions." in driver.find_element(By.TAG_NAME, "body").text:
            print(f"No submissions found on page {page_index}. Stopping...")
            return False
    except NoSuchElementException:
        pass

    raw_text = driver.find_element(By.TAG_NAME, "body").text
    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]

    try:
        start_idx = lines.index("During Contest?") + 1  # Locate table start
    except ValueError:
        print(f"Headers not found on page {page_index}, skipping...")
        return False

    # Extract submission data
    i = start_idx
    while i < len(lines):
        if lines[i] == "View":  # Ignore "View" links
            i += 1
            continue
        row = lines[i:i + 9]
        if len(row) == 9:
            structured_data.append(row)
        i += 9

    print(f"Processed page {page_index}")
    return True  # Continue scraping

# Start scraping pages
page_index = 1
while scrape_page(page_index):
    page_index += 1
    break

# Save data to CSV
CSV_FILENAME = "hackerrank_submissions.csv"
with open(CSV_FILENAME, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(HEADERS)
    writer.writerows(structured_data)

print(f"Data successfully saved to {CSV_FILENAME}")

# Close WebDriver
driver.quit()

### Firebase Integration ###
def initialize_firebase():
    """Initializes Firebase with credentials."""
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred, {"databaseURL": "https://test-round2-default-rtdb.firebaseio.com/"})
    return db.reference("leaderboard")

def update_firebase():
    """Updates Firebase leaderboard based on the scraped data."""
    teams_ref = initialize_firebase()
    df = pd.read_csv(CSV_FILENAME)

    for _, row in df.iterrows():
        team_name = str(row["Team"]).strip()
        status = str(row["Result"]).strip().lower()

        if status == "accepted":  # Only count accepted submissions
            team_ref = teams_ref.child(team_name)
            current_count = team_ref.get() or 0
            team_ref.set(current_count + 1)

    print("Firebase updated successfully!")

update_firebase()
