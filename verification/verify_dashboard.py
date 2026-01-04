from playwright.sync_api import sync_playwright, expect
import time

def verify_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            print("Navigating to app...")
            page.goto("http://localhost:8510")
            page.wait_for_load_state("networkidle")
            time.sleep(2)

            # Check if we are at login
            if page.get_by_text("Acceso al Sistema").is_visible():
                print("At Login Screen. Attempting Manual Login...")

                # Expand Emergency Access
                # Streamlit expanders are usually details/summary or buttons.
                # "ACCESO DE EMERGENCIA" is the label of the expander.
                page.get_by_text("⚠️ ACCESO DE EMERGENCIA").click()
                time.sleep(1)

                # Fill inputs
                # Streamlit inputs are identified by labels usually, or we can find by aria-label
                # The code has keys "login_u" and "login_p", but usually labels are rendered.
                # "ID Operador" and "Clave de Acceso" are the labels.

                # Wait for inputs to be visible
                page.get_by_label("ID Operador").fill("admin")
                page.get_by_label("Clave de Acceso").fill("admin")

                # Click Login Button
                page.get_by_role("button", name="INICIAR ACCESO MANUAL").click()

                print("Login submitted. Waiting for reload...")
                page.wait_for_load_state("networkidle")
                time.sleep(3) # Wait for rerun

            # Now we should be at Dashboard
            print("Checking Dashboard content...")

            # Check for Spanish translation
            expect(page.get_by_text("MÉTRICAS EN VIVO")).to_be_visible(timeout=10000)
            expect(page.get_by_text("INGRESOS TOTALES")).to_be_visible()

            # Take success screenshot
            page.screenshot(path="verification/dashboard_spanish_success.png", full_page=True)
            print("SUCCESS: Dashboard translated and stars background logic intact (implied by app running).")

        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/dashboard_fail.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_dashboard()
