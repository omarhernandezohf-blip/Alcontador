from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    try:
        page.goto("http://localhost:8501")
        # Print the page content to see what's rendering
        print(page.content())
        page.screenshot(path="verification/debug_screenshot.png")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
