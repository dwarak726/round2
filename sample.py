from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import csv

driver = webdriver.Chrome()

base_url = "https://www.hackerrank.com/contests/aac-problem-solving/judge/submissions"
page_index = 1  # Start with "/challenge"

driver.get(base_url + "/challenge")
input("Log in to HackerRank, then press Enter here...")

headers = ["Problem", "Team", "ID", "Language", "Time", "Result", "Score", "Status", "During Contest"]
structured_data = []

while True:
    # Load page
    url = f"{base_url}/{page_index}" if page_index > 1 else base_url + "/challenge"
    driver.get(url)
    print(url)
    time.sleep(3) 

    try:
        # Check for No submissions
        if "There are no submissions." in driver.find_element(By.TAG_NAME, "body").text:
            print(f"No submissions found on page {page_index}. Stopping...")
            break
    except NoSuchElementException:
        pass

    # Extract text
    raw_text = driver.find_element(By.TAG_NAME, "body").text
    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]

    try:
        start_idx = lines.index("During Contest?") + 1  # Skip headers
    except ValueError:
        print(f"Headers not found on page {page_index}, skipping...")
        break

    # Extract data
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
    page_index += 1

csv_filename = "hackerrank_submissions.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)  # Write headers
    writer.writerows(structured_data)  # Write data rows

print(f"Data successfully saved to {csv_filename}")

driver.quit()
