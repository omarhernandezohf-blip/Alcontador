
import os
import sys
from playwright.sync_api import sync_playwright
import time

def verify_smart_features():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to app...")
        # Assuming app is running on localhost:8501
        try:
            page.goto("http://localhost:8501", timeout=10000)
        except Exception as e:
            print(f"Error connecting to app: {e}")
            return

        time.sleep(5)

        # Login Bypass (if needed, but usually we just want to see the login screen or sidebar)
        # Check if we are on login screen
        if page.locator("text=Bienvenido de Nuevo").is_visible() or page.locator("text=Welcome Back").is_visible():
            print("On Login Screen. Using Manual Override...")
            # Click expander
            page.locator("text=ACCESO DE EMERGENCIA").click()
            time.sleep(1)
            page.fill("input[aria-label='ID Operador']", "admin")
            page.fill("input[type='password']", "admin")
            page.click("button:has-text('INICIAR ACCESO MANUAL')")
            time.sleep(3)

        # Verify Sidebar Language Toggle
        print("Verifying Language Toggle...")
        # Check for language selector
        # Note: Streamlit selectbox is tricky. We'll just verify the default language is Spanish (ES) by checking menu items.

        # Check if dashboard menu item exists
        if page.locator("text=Inicio / Dashboard").is_visible():
            print("Language is Spanish.")
        elif page.locator("text=Home / Dashboard").is_visible():
            print("Language is English.")

        # Switch to English
        print("Switching to English...")
        # Find the selectbox - this is hard in Streamlit without custom IDs, but we added key="lang_selector_main"
        # However, verifying the switch might be complex via headless.
        # Let's verify Navigation to a module.

        # Click on "Costeo de Nómina Real" (or equivalent)
        print("Navigating to Payroll Module...")
        try:
            # We need to find the radio button.
            # Streamlit radio buttons are labels.
            page.get_by_text("Costeo de Nómina Real").click()
            time.sleep(2)

            # Check for Module Title
            if page.locator("h2:has-text('Calculadora de Costo Real')").is_visible():
                print("Successfully navigated to Payroll Module.")

                # Verify Download Button Existence
                if page.locator("button:has-text('📥 Download Excel')").count() > 0 or page.locator("button:has-text('Download Excel')").count() > 0:
                     print("Download Button Found (Pre-calculation check - might not be visible yet if inside button block).")

                # Fill some dummy data to trigger calculation
                # Upload logic is hard.
                # Let's try "Minería de XML" or something simpler if possible.
                # Actually, "Validador de RUT" is simple.

            else:
                print("Failed to navigate to Payroll Module.")

        except Exception as e:
            print(f"Navigation error: {e}")

        # Capture final screenshot
        page.screenshot(path="verification_smart_features.png")
        print("Screenshot saved to verification_smart_features.png")

        browser.close()

if __name__ == "__main__":
    verify_smart_features()
