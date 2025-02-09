
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
    # Launch browser with no-sandbox flag for better compatibility in CI/CD
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])

    # Create a new browser context
    context = browser.new_context()

    # Set the user-agent for the context
    context.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Open a new page within the context
    page = context.new_page()

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
