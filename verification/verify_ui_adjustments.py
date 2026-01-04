import os
import time
from playwright.sync_api import sync_playwright

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the app (assuming it's running locally on port 8501)
        # Note: In the actual environment, we might need to ensure the app is running.
        # But for this script, we assume the server is up.
        try:
            page.goto("http://localhost:8501", timeout=30000)
            page.wait_for_load_state("networkidle")

            # Allow some time for Streamlit to render
            time.sleep(5)

            # --- VERIFY SIDEBAR TOGGLE ---
            print("Verifying Sidebar Toggle...")
            sidebar_toggle = page.locator('[data-testid="stSidebarCollapsedControl"]')

            if sidebar_toggle.count() > 0:
                # Get computed styles
                z_index = sidebar_toggle.evaluate("element => getComputedStyle(element).zIndex")
                color = sidebar_toggle.evaluate("element => getComputedStyle(element).color")
                border = sidebar_toggle.evaluate("element => getComputedStyle(element).border")

                print(f"Sidebar Toggle Z-Index: {z_index}")
                print(f"Sidebar Toggle Color: {color}")
                print(f"Sidebar Toggle Border: {border}")

                # Check against requirements
                if z_index != "9999999":
                     print("FAILURE: Sidebar z-index incorrect.")
                else:
                     print("SUCCESS: Sidebar z-index correct.")

                if "255, 255, 255" in color or "rgb(255, 255, 255)" in color:
                     print("SUCCESS: Sidebar color correct.")
                else:
                     print(f"FAILURE: Sidebar color incorrect ({color}).")

            else:
                print("FAILURE: Sidebar toggle not found.")

            # --- VERIFY LOGIN BUTTON CENTERING ---
            print("\nVerifying Login Button Centering...")
            # The button is likely inside a div[data-testid="stButton"]
            # We injected CSS to center it.
            login_btn_container = page.locator('div[data-testid="stButton"]').first

            if login_btn_container.count() > 0:
                display = login_btn_container.evaluate("element => getComputedStyle(element).display")
                justify = login_btn_container.evaluate("element => getComputedStyle(element).justifyContent")

                print(f"Login Button Display: {display}")
                print(f"Login Button Justify: {justify}")

                if display == "flex" and justify == "center":
                    print("SUCCESS: Login button is centered via flexbox.")
                else:
                    print("FAILURE: Login button centering styles missing.")
            else:
                print("WARNING: Login button container not found (might need to wait longer or element ID changed).")

            # Take a screenshot
            if not os.path.exists("verification"):
                os.makedirs("verification")
            page.screenshot(path="verification/ui_verification.png")
            print("\nScreenshot saved to verification/ui_verification.png")

        except Exception as e:
            print(f"Verification failed with error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()
