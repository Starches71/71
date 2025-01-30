
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# YouTube video link
YT_LINK = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# YouTube downloader site
DOWNLOADER_URL = "https://ssyoutube.com"

# Setup Chrome options for headless mode (for GitHub Actions)
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

    # Wait for the input box to appear
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))  # Update selector if needed
    )
    
    # Paste the YouTube link
    input_box.send_keys(YT_LINK)
    input_box.send_keys(Keys.RETURN)

    # Wait for the download button to appear
    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'download')]"))  # Update selector if needed
    )
    
    # Click the download button
    download_button.click()

    print("✅ Download Successful!")

except Exception as e:
    print(f"❌ Download failed: {e}")

finally:
    driver.quit()
