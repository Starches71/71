
from playwright.sync_api import sync_playwright
import time

EMAIL = "starches131@gmail.com"
PASSWORD = "bajubwoy131#"

def print_all_elements(page):
    # Print all elements' IDs and text content to help debug the issue
    elements = page.query_selector_all('*')
    for element in elements:
        id = element.get_attribute('id')
        text = element.inner_text()
        if id:
            print(f"Element ID: {id} - Text: {text}")
        else:
            print(f"Element without ID - Text: {text}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Set to True for GitHub Actions
    page = browser.new_page()
    
    # Navigate to Gmail login page
    page.goto("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&hl=en&service=mail&flowName=GlifWebSignIn&flowEntry=AddSession")

    try:
        # Enter email
        page.fill("input#identifierId", EMAIL)
        page.click("text=Next")
        time.sleep(3)

        # Enter password (wait for it to load)
        page.fill("input[name='Passwd']", PASSWORD)
        page.click("text=Next")
        time.sleep(3)

        print("Login attempted. Check browser for results.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Printing all page elements for debugging...")
        print_all_elements(page)
    
    browser.close()
