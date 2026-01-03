
import os
import sys
from playwright.sync_api import sync_playwright
import time

def verify_module_guides():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to app...")
        try:
            page.goto("http://localhost:8501", timeout=10000)
        except Exception as e:
            print(f"Error connecting to app: {e}")
            return

        time.sleep(5)

        # Login Bypass
        if page.locator("text=Bienvenido de Nuevo").is_visible() or page.locator("text=Welcome Back").is_visible():
            print("On Login Screen. Using Manual Override...")
            page.locator("text=ACCESO DE EMERGENCIA").click()
            time.sleep(1)
            page.fill("input[aria-label='ID Operador']", "admin")
            page.fill("input[type='password']", "admin")
            page.click("button:has-text('INICIAR ACCESO MANUAL')")
            time.sleep(3)

        # Test 1: Payroll Module Guide
        print("Navigating to Payroll Module...")
        try:
            page.get_by_text("Costeo de Nómina Real").click()
            time.sleep(2)

            if page.locator("text=Module Guide").is_visible():
                print("✅ Module Guide Title Visible")
            else:
                print("❌ Module Guide Title NOT Visible")

            if page.locator("text=Calculate the exact total cost").is_visible():
                print("✅ Payroll Purpose Visible")
            else:
                print("❌ Payroll Purpose NOT Visible")

        except Exception as e:
            print(f"Navigation error: {e}")

        # Test 2: DIAN Audit Module Guide
        print("Navigating to DIAN Module...")
        try:
            page.get_by_text("Auditoría Cruce DIAN").click()
            time.sleep(2)

            if page.locator("text=Prevent penalties for inaccuracy").is_visible():
                print("✅ DIAN Benefits Visible")
            else:
                print("❌ DIAN Benefits NOT Visible")

        except Exception as e:
            print(f"Navigation error: {e}")

        # Capture final screenshot
        page.screenshot(path="verification_guides.png")
        print("Screenshot saved to verification_guides.png")

        browser.close()

if __name__ == "__main__":
    verify_module_guides()
