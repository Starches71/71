from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Hardcoded credentials (NOT RECOMMENDED)
EMAIL = "starches171@gmail.com"
PASSWORD = "is-haqkabaju"

# Save cookies to a Netscape-style cookies.txt file
def save_cookies_to_netscape(cookies, output_file):
    with open(output_file, 'w') as file:
        file.write("# Netscape HTTP Cookie File\n")
        for cookie in cookies:
            file.write(
                f"{cookie['domain']}\t"
                f"TRUE\t"
                f"{cookie['path']}\t"
                f"FALSE\t"
                f"{int(cookie['expiry']) if 'expiry' in cookie else 0}\t"
                f"{cookie['name']}\t"
                f"{cookie['value']}\n"
            )

# Setup WebDriver
options = Options()
options.add_argument("--headless")  # Optional: Run Chrome in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    # Open YouTube login page
    driver.get("https://www.youtube.com")
    time.sleep(2)

    # Click Sign In
    driver.find_element(By.XPATH, '//*[@id="buttons"]/ytd-button-renderer/a').click()
    time.sleep(2)

    # Enter Email
    driver.find_element(By.ID, "identifierId").send_keys(EMAIL)
    driver.find_element(By.ID, "identifierNext").click()
    time.sleep(2)

    # Enter Password
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "passwordNext").click()
    time.sleep(5)

    # Save Cookies
    cookies = driver.get_cookies()
    save_cookies_to_netscape(cookies, "cookies.txt")
    print("Cookies saved to cookies.txt")

finally:
    driver.quit()