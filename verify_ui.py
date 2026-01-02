from playwright.sync_api import sync_playwright
import time
import os

def run():
    print("Starting Streamlit app...")
    # Run Streamlit in the background
    os.system("python3 -m streamlit run app.py --server.port 8501 --server.headless true > streamlit.log 2>&1 &")

    print("Waiting for app to launch...")
    time.sleep(5)  # Give it time to start

    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch()
        page = browser.new_page()

        print("Navigating to app...")
        page.goto("http://localhost:8501")

        print("Waiting for content to load...")
        # Wait for the main app container
        page.wait_for_selector(".stApp", timeout=10000)

        # Additional wait to ensure fonts and styles are applied
        time.sleep(3)

        print("Taking screenshot...")
        if not os.path.exists("verification"):
            os.makedirs("verification")

        page.screenshot(path="verification/verification_final.png", full_page=True)
        print("Screenshot taken: verification/verification_final.png")

        browser.close()

    print("Stopping app...")
    os.system("pkill -f streamlit")

if __name__ == "__main__":
    run()
