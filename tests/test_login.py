import yaml
from playwright.sync_api import sync_playwright

# Load YAML config
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config["headless"])
        page = browser.new_page()

        # Navigate to the login page
        page.goto(f"{config['base_url']}/login")

        # Wait for the email input field to appear
        page.wait_for_selector('#email')

        # Perform login
        page.fill('#email', config["credentials"]["username"])
        page.fill('[name="pass"]', config["credentials"]["password"])

        # Wait for the login button and click it
        page.wait_for_selector('[name="login"]')
        page.click('[name="login"]')

        # Check if 'Wrong credentials' message appears
        if page.get_by_text("Wrong credentials").is_visible():
            print("Login failed: Wrong credentials")
        else:
            
            print("Login succeeded")

            browser.close()
