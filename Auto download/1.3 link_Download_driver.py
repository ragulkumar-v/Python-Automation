from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# Configuration
URL = "https://www.kezarmarkets.com/disclosure-of-sec-required-order-execution-information/"
SAVE_DIRECTORY = "C:/RA work/SEC Rule 605 Datasets/EXBL"
SAVE_FILE = "extracted_links.txt"

# Ensure the directory exists
if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)

SAVE_PATH = os.path.join(SAVE_DIRECTORY, SAVE_FILE)

def extract_links_with_selenium():
    """Extracts links using Selenium and saves them to a file."""
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(URL)
        time.sleep(5)  # Wait for JavaScript to load the page

        # Extract all links matching the pattern
        extracted_links = [
            a.get_attribute("href") for a in driver.find_elements(By.TAG_NAME, "a")
            if a.get_attribute("href") and a.get_attribute("href").startswith("https://www.kezarmarkets.com/wp-content/uploads/")
            
        ]

        # Save extracted links to a file
        with open(SAVE_PATH, "w", encoding="utf-8") as file:
            for link in extracted_links:
                file.write(link + "\n")

        print(f"Successfully saved {len(extracted_links)} links to {SAVE_PATH}")

    except Exception as e:
        print(f"Error fetching the webpage: {str(e)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    extract_links_with_selenium()
