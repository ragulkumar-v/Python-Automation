from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

# Configuration
URL = "https://www.kezarmarkets.com/disclosure-of-sec-required-order-execution-information/"  # Change to the actual URL where ZIP files are listed
DOWNLOAD_DIRECTORY = "C:/RA work/SEC Rule 605 Datasets/EXBL"  # Set your target folder

# Ensure the directory exists
if not os.path.exists(DOWNLOAD_DIRECTORY):
    os.makedirs(DOWNLOAD_DIRECTORY)

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": os.path.abspath(DOWNLOAD_DIRECTORY),  # Set download directory
    "download.prompt_for_download": False,  # Disable download prompt
    "safebrowsing.enabled": True  # Ensure safe browsing is enabled
})

# Initialize Selenium WebDriver
driver = webdriver.Chrome(options=options)
try:
    # Open the target webpage
    driver.get(URL)
    time.sleep(3)  # Wait for the page to load

    # Find all links that end with .zip
    zip_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.zip')]")

    print(f"Found {len(zip_links)} zip files to download.")

    for link in zip_links:
        try:
            file_name = link.text.strip()  # Get file name
            print(f"Downloading: {file_name}")

            # Click the link to initiate download
            link.click()

            # Wait some time for the download to complete (adjust based on file size)
            time.sleep(5)

        except Exception as e:
            print(f"Error downloading {file_name}: {str(e)}")
            continue

    print("All downloads completed.")

finally:
    driver.quit()
