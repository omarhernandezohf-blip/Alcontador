import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Using a fixed viewport to simulate a desktop screen
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        # Navigate to local Streamlit app
        page.goto("http://localhost:8501")

        # Wait for the app to load
        # We look for the Login Title "Asistente Contable PRO" (checking partial text)
        page.wait_for_selector('h1:has-text("Asistente Contable")', timeout=10000)

        # 1. Verify Spanish Strings
        content = page.content()
        if "Asistente Contable" in content and "v14.5 Suite Empresarial" in content:
            print("SUCCESS: Found Spanish Login Title/Subtitle")
        else:
            print("FAILURE: Did not find Spanish Login strings")

        # 2. Verify Language Selector in Sidebar
        # The sidebar might be collapsed or open. We check if the selectbox label exists.
        # Streamlit selectbox labels are usually in a <label> or div.
        # We look for "Language / Idioma"

        # First, try to open sidebar if it's collapsed (though we set initial_sidebar_state="expanded")
        # But let's check existence first.

        if "Language / Idioma" in content:
            print("SUCCESS: Found Language Selector")
        else:
             print("FAILURE: Did not find Language Selector")

        # Take screenshot
        page.screenshot(path="verification/login_page_ui.png")
        print("Screenshot saved to verification/login_page_ui.png")

        browser.close()

if __name__ == "__main__":
    run()
