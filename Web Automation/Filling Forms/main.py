from playwright.sync_api import sync_playwright
import os

filepath = "file://" + os.path.abspath("order_form.html")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(filepath)

    # Step 1
    page.select_option("#product", "sourdough")
    page.fill("#quantity", "3")
    page.click("#next-btn")

    # Step 2
    page.fill("#customer-name", "Priya Shah")
    page.fill("#customer-email", "priya@example.com")
    page.check("#delivery")
    page.check("#gift-wrap")
    page.click("#place-order-btn")

    # Confirmation
    page.wait_for_selector("#confirmation", state="visible")
    print(page.inner_text("#confirmation-details"))

    browser.close()