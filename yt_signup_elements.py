from playwright.sync_api import sync_playwright
import time

# Hardcoded credentials (HIGHLY INSECURE – Use a safer method in real applications)
EMAIL = "starches131@gmail.com"
PASSWORD = "bajubwoy131#"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set to False to see the process
    page = browser.new_page()
    
    # Navigate to Gmail login page
    page.goto("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&hl=en&service=mail&flowName=GlifWebSignIn&flowEntry=AddSession")

    # Enter email
    page.fill("input#identifierId", EMAIL)
    page.click("text=Next")
    time.sleep(3)

    # Enter password (wait for it to load)
    page.fill("input[name='Passwd']", PASSWORD)
    page.click("text=Next")
    time.sleep(3)

    print("Login attempted. Check browser for results.")
    
    # Keep the browser open for testing (remove if not needed)
    time.sleep(10)
    
    browser.close()
