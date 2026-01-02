from playwright.sync_api import sync_playwright

def verify_gatekeeper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            # Navigate to the app (assuming default port 8501)
            page.goto("http://localhost:8501", timeout=10000)

            # Wait for content to load
            page.wait_for_selector("text=SYSTEM ACCESS", timeout=15000)

            # Verify specific UI elements of the Gatekeeper
            assert page.is_visible("text=AUTHENTICATION REQUIRED FOR ENTERPRISE SUITE")
            assert page.is_visible("text=🔐 INICIAR SESIÓN CON GOOGLE")

            # Take screenshot
            page.screenshot(path="verification/gatekeeper_locked.png")
            print("Verification successful: gatekeeper_locked.png created.")

        except Exception as e:
            print(f"Verification failed: {e}")
            # Take screenshot anyway to debug
            page.screenshot(path="verification/debug_fail.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_gatekeeper()
