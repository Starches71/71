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

    # Wait for the page to load
    time.sleep(3)

    # Close the pop-up if it appears
    try:
        close_popup = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.widget > div.widget__overlay > div.widget__container > button.widget__button.widget__button--close > img.widget__icon"))
        )
        close_popup.click()
        print("✅ Closed pop-up successfully.")
    except Exception:
        print("ℹ️ No pop-up detected, continuing.")

    # Wait for the input box and enter the YouTube link
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#id_url"))
    )
    input_box.send_keys(YT_LINK)
    
    # Click the search button
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#search > i.fas.fa-arrow-right"))
    )
    search_button.click()
    print("✅ Video URL submitted.")

    # Wait for the download button (We need its exact selector)
    time.sleep(5)  # Adjust based on how long the site takes to process

    print("✅ Download should now be available (provide the download button selector).")

except Exception as e:
    print(f"❌ Download failed: {e}")

finally:
    driver.quit()
