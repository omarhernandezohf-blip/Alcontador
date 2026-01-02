from playwright.sync_api import sync_playwright
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    try:
        page.goto("http://localhost:8501")
        # Wait a bit for streamlit to hydrate
        time.sleep(5)

        # Check for the button OR the offline message
        # We expect "GOOGLE AUTH OFFLINE" because we don't have secrets in the sandbox
        if page.locator("text=GOOGLE AUTH OFFLINE").count() > 0:
            print("Found Offline Message - Correct for Sandbox")
            page.screenshot(path="verification/login_screen_fixed.png")
        elif page.locator("button:has-text('Sign in with Google')").count() > 0:
            print("Found Login Button")
            page.screenshot(path="verification/login_screen_fixed.png")
        else:
            print("Found neither!")
            page.screenshot(path="verification/error_screenshot.png")

    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="verification/error_screenshot.png")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
