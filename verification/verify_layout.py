from playwright.sync_api import sync_playwright
import time

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 720})

        print("Navigating to app...")
        page.goto("http://localhost:8501")

        # Wait for the title to appear, indicating the app has loaded
        print("Waiting for load...")
        try:
            page.wait_for_selector("h1", timeout=10000)
        except:
            print("Timeout waiting for h1. Dumping content...")
            # print(page.content())

        # Take a screenshot of the initial login page
        print("Taking login screenshot...")
        page.screenshot(path="verification/login_page_initial.png")

        # Check sidebar state
        # Sidebar selector in recent streamlit versions is usually section[data-testid="stSidebar"]
        sidebar = page.locator('section[data-testid="stSidebar"]')

        # Check if sidebar is expanded (width > 0 or visible)
        box = sidebar.bounding_box()
        print(f"Sidebar box: {box}")

        # Take screenshot of the sidebar area specifically
        page.screenshot(path="verification/sidebar_initial.png", clip={'x':0, 'y':0, 'width': 400, 'height': 720})

        # Check for toggle button
        toggle = page.locator('[data-testid="stSidebarCollapsedControl"]')
        if toggle.count() > 0:
             print("Toggle button found.")
             # Take screenshot of the toggle button area
             toggle_box = toggle.bounding_box()
             if toggle_box:
                 print(f"Toggle box: {toggle_box}")
                 # Expand clip slightly to see surroundings
                 clip = {'x': max(0, toggle_box['x']-10), 'y': max(0, toggle_box['y']-10), 'width': toggle_box['width']+20, 'height': toggle_box['height']+20}
                 page.screenshot(path="verification/sidebar_toggle_initial.png", clip=clip)
        else:
             print("Toggle button NOT found.")

        browser.close()

if __name__ == "__main__":
    run_verification()
