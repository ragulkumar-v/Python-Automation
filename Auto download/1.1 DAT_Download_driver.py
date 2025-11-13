import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configuration
DOWNLOAD_DIRECTORY = "C:/RA work/SEC Rule 605 Datasets/EXBL"
LOG_FILE = "processed_files_log.txt"
FILE_LINKS = ["https://www.kezarmarkets.com/wp-content/uploads/2025/02/EBXL2025_Jan605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2025/01/EBXL2024_Dec605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2024/12/EBXL2024_Nov605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2024/11/EBXL202404_Oct605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2024/10/EBXL202404_Sep605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2024/09/EBXL202404_Aug605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2024/07/EBXL202404_Jun605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2024/06/EBXL202404_May605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2024/05/EBXL202404_Apr605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2024/05/EBXL202403_Mar605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2024/03/EBXL202402_Feb605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2024/02/EBXL202401_Jan605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2024/01/EBXL202312_Dec605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/12/EBXL202311_Nov605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/12/EBXL202310_Oct605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/10/EBXL202309_Sep605.txt.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/10/EBXL202308_Aug605.txt.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/08/EBXL202307_July605.txt.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/08/EBXL202306_June605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/06/EBXL202305_May605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/06/EBXL202304_Apr605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/04/EBXL202303_Mar605.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202302_Feb605_zip-284-52466-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202301_Jan605_zip-284-52400-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202212_DEC605_zip-284-52299-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202211_NOV605_zip-284-52272-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202210_OCT605_zip-284-52118-1-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202209_SEP605_zip-284-52018-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202208_AUG605_zip-284-51955-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202207_JUL605_zip-284-51867-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202206_JUN605_zip-284-51868-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202205_MAY605_zip-284-51542-1-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202204_APR605_zip-284-51416-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202203_MAR605_zip-284-51264-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202202_FEB605_zip-284-51265-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202201_JAN605_zip-284-51069-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202112_DEC605_zip-284-51006-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202111_NOV605_zip-284-51005-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202110_OCT605_zip-284-50819-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202109_SEP605_zip-284-50754-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202108_AUG605_zip-284-50668-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202107_JULY605_zip-284-50515-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202105_JUNE605_zip-284-50462-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202105_MAY605_zip-284-50409-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202104_April605_zip-284-50214-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202103_March605_zip-284-50155-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202102_FEBRUARY2021_zip-284-50044-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202101_JANUARY2021_dat_zip-284-49999-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202012_DECEMBER605_zip-284-49989-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202011_NOVEMBER605_zip-284-49915-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202010_OCTOBER605_zip-284-49856-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202009_SEPTEMBER605_zip-284-49818-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202008_AUGUST605_zip-284-49817-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202007_JULY605_zip-284-49816-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202006_JUNE605_zip-284-49815-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202005_MAY605_zip-284-49814-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202004_APRIL605_zip-284-49813-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202003_MARCH605_zip-284-49812-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202002_FEBRUARY605_zip-284-49811-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202001_JANUARY605_zip-284-49810-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL201912_DECEMBER605_zip-284-49821-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL201911_NOVEMBER605_zip-284-49822-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL201910_OCTOBER605_zip-284-49823-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL201909_SEPTEMBER605_zip-284-49824-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL201908_AUGUST605_zip-284-49825-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL201907_JULY605_zip-284-49826-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL201906_JUNE605_zip-284-49827-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL201905_MAY605_zip-284-49828-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202212_DEC605_zip-284-52299-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202211_NOV605_zip-284-52272-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202210_OCT605_zip-284-52118-1-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202209_SEP605_zip-284-52018-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202208_AUG605_zip-284-51955-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202207_JUL605_zip-284-51867-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202206_JUN605_zip-284-51868-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202205_MAY605_zip-284-51542-1-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202204_APR605_zip-284-51416-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202203_MAR605_zip-284-51264-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202202_FEB605_zip-284-51265-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202201_JAN605_zip-284-51069-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202212_DEC605_zip-284-52299-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202211_NOV605_zip-284-52272-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202210_OCT605_zip-284-52118-1-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202209_SEP605_zip-284-52018-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202208_AUG605_zip-284-51955-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202207_JUL605_zip-284-51867-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202206_JUN605_zip-284-51868-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202205_MAY605_zip-284-51542-1-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202204_APR605_zip-284-51416-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202203_MAR605_zip-284-51264-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202202_FEB605_zip-284-51265-1.zip",
"https://www.kezarmarkets.com/wp-content/uploads/2023/03/Current-EBXL202201_JAN605_zip-284-51069-1.zip",
]

# Ensure download directory exists
if not os.path.exists(DOWNLOAD_DIRECTORY):
    os.makedirs(DOWNLOAD_DIRECTORY)

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def setup_driver():
    """Set up and return a Selenium WebDriver instance."""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def extract_and_save_file(driver, file_url):
    """Extracts text content from a URL and saves it as a .dat file."""
    try:
        driver.get(file_url)
        time.sleep(3)  # Allow the page to load
        
        # Extract text content from the page
        content = driver.find_element(By.TAG_NAME, "body").text
        
        # Extract filename from URL
        file_name = file_url.split("/")[-1].split(".")[0] + ".zip"
        file_path = os.path.join(DOWNLOAD_DIRECTORY, file_name)
        
        # Save the extracted content
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        
        logging.info(f"Successfully processed: {file_name}")
        print(f"Downloaded and saved: {file_name}")
    except Exception as e:
        logging.error(f"Failed to process {file_url}: {str(e)}")
        print(f"Error processing {file_url}: {str(e)}")

def main():
    """Main function to automate file extraction and saving."""
    driver = setup_driver()
    
    print(f"Starting processing of {len(FILE_LINKS)} files...")
    
    for file_url in FILE_LINKS:
        extract_and_save_file(driver, file_url)
        time.sleep(2)  # Configurable delay
    
    driver.quit()
    print("All files processed successfully.")

if __name__ == "__main__":
    main()
