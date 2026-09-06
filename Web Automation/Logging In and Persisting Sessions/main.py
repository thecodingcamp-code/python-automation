import os
from playwright.sync_api import sync_playwright

url = "http://localhost:8199/dashboard.html"
STATE_FILE = "auth_state.json"

def login_and_save_state(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    page.fill("#username", "demo")
    page.fill("#password", "demo123")
    page.click("#login-btn")
    page.wait_for_selector("#dashboard", state="visible")
    context.storage_state(path=STATE_FILE)
    return context, page

with sync_playwright() as p:
    browser = p.chromium.launch()

    if os.path.exists(STATE_FILE):
        print("Found saved session, reusing it")
        context = browser.new_context(storage_state=STATE_FILE)
        page = context.new_page()
        page.goto(url)
    else:
        print("No saved session found, logging in fresh")
        context, page = login_and_save_state(browser)

    print("Dashboard visible:", page.is_visible("#dashboard"))
    context.close()
    browser.close()