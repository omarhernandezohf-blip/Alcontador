from playwright.sync_api import sync_playwright, expect
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Note: In a real environment, we'd assume the server is already running.
        # Here we just connect to the local port where Streamlit should be running.
        page = browser.new_page()

        try:
            # Navigate to local streamlit app
            page.goto("http://localhost:8501")

            # Wait for content to load
            page.wait_for_selector("text=Acceso al Sistema", timeout=10000)

            # Verify Spanish strings
            expect(page.get_by_text("Acceso al Sistema")).to_be_visible()
            expect(page.get_by_text("Autenticación requerida para Enterprise Suite")).to_be_visible()

            # Verify the manual override section translation
            expect(page.get_by_text("ACCESO DE EMERGENCIA")).to_be_visible()

            # Verify the OFFLINE message translation (New check)
            expect(page.get_by_text("⚠️ AUTENTICACIÓN GOOGLE NO DISPONIBLE")).to_be_visible()

            # Take screenshot
            page.screenshot(path="verification/login_spanish_v2.png")
            print("Verification successful! Screenshot saved to verification/login_spanish_v2.png")

        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/failure.png")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
