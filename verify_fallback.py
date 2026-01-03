from playwright.sync_api import sync_playwright

def verify_fallback_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            # Navigate to the app (assuming default port 8501)
            page.goto("http://localhost:8501", timeout=10000)

            # Wait for content to load
            page.wait_for_selector("text=SYSTEM ACCESS", timeout=15000)

            # 1. Verify "EMERGENCY OVERRIDE" expander exists
            assert page.is_visible("text=⚠️ EMERGENCY OVERRIDE")

            # 2. Click the expander to open it
            page.click("text=⚠️ EMERGENCY OVERRIDE")

            # 3. Wait for inputs to be visible
            page.wait_for_selector("input[aria-label='Operator ID']", timeout=2000)

            # 4. Fill credentials (admin/admin)
            page.fill("input[aria-label='Operator ID']", "admin")
            page.fill("input[aria-label='Access Key']", "admin")

            # 5. Click "INITIATE MANUAL OVERRIDE"
            # Streamlit buttons sometimes have specific structures, usually role='button' and name matching text
            page.click("button:has-text('INITIATE MANUAL OVERRIDE')")

            # 6. Wait for dashboard to load (look for sidebar user info or dashboard specific text)
            # The dashboard shows "OPERATOR: Admin (Manual)" in the sidebar
            page.wait_for_selector("text=OPERATOR:", timeout=15000)
            page.wait_for_selector("text=Admin (Manual)", timeout=5000)

            print("Login successful! Dashboard accessed via Fallback.")

            # Take screenshot of the Dashboard
            page.screenshot(path="verification/dashboard_unlocked.png")

        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/fallback_fail.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_fallback_login()
