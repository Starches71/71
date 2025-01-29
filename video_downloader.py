
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# YouTube video link (replace with any valid YouTube URL)
YT_LINK = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Choose an online downloader (update if needed)
DOWNLOADER_URL = "https://ssyoutube.com"

# Setup Chrome options for headless mode (required for GitHub Actions)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1200")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Start WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the YouTube downloader site
    driver.get(DOWNLOADER_URL)
    time.sleep(3)  # Allow page to load

    # Find the input box and paste YouTube link
    input_box = driver.find_element(By.NAME, "q")  # Might need to update selector
    input_box.send_keys(YT_LINK)
    input_box.send_keys(Keys.RETURN)

    time.sleep(5)  # Wait for processing

    # Find the download button
    download_button = driver.find_element(By.XPATH, "//a[contains(@class, 'download-button')]")  # Might need updating
    download_button.click()

    print("✅ Download Successful!")
except Exception as e:
    print(f"❌ Download failed: {e}")

finally:
    driver.quit()
