from playwright.sync_api import sync_playwright, expect
import time

def verify_sidebar_visibility():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use a mobile-like viewport to test responsiveness/collapsed state handling if needed,
        # but the request is for PC and Mobile. Standard desktop size covers PC.
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        try:
            print("Navigating to app...")
            page.goto("http://localhost:8510")
            page.wait_for_load_state("networkidle")
            time.sleep(2)

            # 1. Login Logic (Copied from previous success)
            if page.get_by_text("Acceso al Sistema").is_visible():
                print("At Login Screen. Attempting Manual Login...")
                page.get_by_text("⚠️ ACCESO DE EMERGENCIA").click()
                time.sleep(0.5)
                page.get_by_label("ID Operador").fill("admin")
                page.get_by_label("Clave de Acceso").fill("admin")
                page.get_by_role("button", name="INICIAR ACCESO MANUAL").click()
                print("Login submitted. Waiting for reload...")
                page.wait_for_load_state("networkidle")
                time.sleep(3)

            # 2. Check Sidebar State
            print("Checking Sidebar...")

            # Identify sidebar elements
            sidebar = page.locator('[data-testid="stSidebar"]')
            collapsed_control = page.locator('[data-testid="stSidebarCollapsedControl"]')

            # Since we set initial_sidebar_state="expanded", the sidebar should be visible.
            expect(sidebar).to_be_visible()

            # Screenshot of the whole page to see the sidebar
            page.screenshot(path="verification/sidebar_visible.png", full_page=True)
            print("Sidebar is visible (Expanded state confirmed).")

            # 3. Collapse Sidebar to check the "Open" button (The critical missing UI element)
            # Find the expand/collapse button inside the open sidebar (usually an X or arrow)
            # Streamlit uses [data-testid="stSidebarExpandedControl"] (arrow) to close it.
            # But the user reported the "open/close button disappeared".
            # If open, we see stSidebarExpandedControl. If closed, we see stSidebarCollapsedControl.

            # Let's try to close it
            close_btn = page.locator('[data-testid="stSidebarExpandedControl"]') # The close arrow
            if close_btn.is_visible():
                print("Closing sidebar to test collapsed control visibility...")
                close_btn.click()
                time.sleep(1)

            # Now sidebar should be collapsed. Check for the "Open" button (stSidebarCollapsedControl)
            # This is the one we styled with high z-index and blue background.
            expect(collapsed_control).to_be_visible()

            # Screenshot of the collapsed state showing the button
            page.screenshot(path="verification/sidebar_collapsed_button_visible.png", full_page=True)
            print("Collapsed Control Button is visible.")

        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/sidebar_fail.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_sidebar_visibility()
