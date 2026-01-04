import os
import time
from playwright.sync_api import sync_playwright

def verify_fix():
    print("Starting Playwright verification...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Go to local streamlit app
        try:
            print("Navigating to http://localhost:8501...")
            # Increased timeout to 60s for slow startup
            page.goto("http://localhost:8501", timeout=60000)

            # Wait for body to ensure page loaded
            print("Waiting for body...")
            page.wait_for_selector("body", timeout=60000)

            # Wait for specific Streamlit elements to ensure full load
            # Often apps show "Please wait..."
            time.sleep(5)

            # Take screenshot
            os.makedirs("verification", exist_ok=True)
            screenshot_path = "verification/login_fix.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved to {screenshot_path}")

            # Check for button
            # Note: The button is inside an iframe if using oauth2 component?
            # Or just a button in a column.
            # We look for the button text "Iniciar sesión con Google"

            # Simple check if text exists
            content = page.content()
            if "Iniciar sesión con Google" in content:
                print("SUCCESS: Login button text found on page.")
            else:
                print("WARNING: Login button text NOT found (might be loading or inside iframe).")

        except Exception as e:
            print(f"Error during verification: {e}")
            page.screenshot(path="verification/error_fix.png")

        finally:
            browser.close()

if __name__ == "__main__":
    verify_fix()
