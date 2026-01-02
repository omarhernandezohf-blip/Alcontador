from playwright.sync_api import sync_playwright

def verify_login_render():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            # Navigate to the app (assuming default port 8501)
            page.goto("http://localhost:8501", timeout=10000)

            # Wait for content to load
            page.wait_for_selector("text=SYSTEM ACCESS", timeout=15000)

            # Verify that the raw HTML code is NOT visible
            # The raw code started with "<a href="
            content = page.content()
            if "&lt;a href=" in content or "&lt;button" in content:
                 print("FAILURE: Raw HTML tags detected in page content!")
            else:
                 print("SUCCESS: No raw HTML tags detected.")

            # Take screenshot of the Login Screen
            page.screenshot(path="verification/login_screen_fixed.png")

        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/login_render_fail.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_login_render()
