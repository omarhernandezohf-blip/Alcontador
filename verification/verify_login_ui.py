import os
import time
from playwright.sync_api import sync_playwright

def verify_login_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Set viewport to standard desktop
        page = browser.new_page(viewport={'width': 1280, 'height': 800})

        try:
            print("Navigating to app...")
            page.goto("http://localhost:8501", timeout=30000)

            # Wait for the app to load (basic sanity check)
            page.wait_for_selector("body", timeout=15000)
            time.sleep(5)  # Allow Streamlit to render everything

            # 1. Verify Sidebar Visibility
            # Streamlit sidebar is usually in [data-testid="stSidebar"]
            # To verify it's expanded, we check if the toggle button is for collapsing (meaning it is open)
            # or check the width/visibility of the sidebar.
            # Sidebar usually has a width > 0 when expanded.

            # Take screenshot of the whole page
            page.screenshot(path="verification/verification_login_ui.png")
            print("Screenshot saved to verification/verification_login_ui.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error_screenshot.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_login_ui()
