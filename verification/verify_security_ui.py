from playwright.sync_api import sync_playwright
import time

def verify_security():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the app (assuming it defaults to login)
        page.goto("http://localhost:8501")

        # Wait for the privacy message
        try:
            page.wait_for_selector("text=Privacidad y Seguridad", timeout=5000)
            print("Privacy message found.")
        except:
            print("Privacy message NOT found.")

        # Take a screenshot
        page.screenshot(path="verification/security_login.png")

        browser.close()

if __name__ == "__main__":
    verify_security()
