import os
import time
from playwright.sync_api import sync_playwright

def verify_ui_strings():
    print("Starting Streamlit app for UI verification...")
    # Assume the app is already running on port 8501 or we start it.
    # In this environment, I usually need to start it.
    # But usually the agent runs a separate command.
    # For now, I will assume I need to launch the browser against the standard port.

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto("http://localhost:8501")
            page.wait_for_timeout(5000) # Wait for load

            content = page.content()

            # Check for Spanish Strings
            has_login_title = "Acceso al Sistema" in content
            has_sidebar_op = "OPERADOR:" in content
            has_logout = "CERRAR SESIÓN" in content

            # Check for English artifacts (Should NOT be present)
            has_terminate = "TERMINATE SESSION" in content
            has_system_access = "System Access" in content

            print(f"Has Login Title ('Acceso al Sistema'): {has_login_title}")
            print(f"Has Sidebar Operator ('OPERADOR:'): {has_sidebar_op}")
            print(f"Has Logout ('CERRAR SESIÓN'): {has_logout}")
            print(f"Has 'TERMINATE SESSION' (Should be False): {has_terminate}")
            print(f"Has 'System Access' (Should be False): {has_system_access}")

            # Verify Logic
            success = False
            if has_login_title:
                print("✅ Login Page detected in Spanish.")
                success = True
            elif has_sidebar_op and has_logout:
                print("✅ Dashboard detected in Spanish.")
                success = True

            if has_terminate or has_system_access:
                print("❌ FAILED: English strings detected.")
                success = False

            if success:
                print("✅ VERIFICATION PASSED: UI is in Spanish.")
            else:
                print("❌ VERIFICATION FAILED: Could not confirm Spanish UI or found English.")

            page.screenshot(path="verification/ui_spanish_check.png")

        except Exception as e:
            print(f"Error during verification: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_ui_strings()
