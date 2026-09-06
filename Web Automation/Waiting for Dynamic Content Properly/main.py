from playwright.sync_api import sync_playwright
import os, time

filepath = "file://" + os.path.abspath("live_feed.html")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(filepath)

    start = time.time()
    page.wait_for_selector(".feed-item")
    elapsed = time.time() - start

    items = page.locator(".feed-item").count()
    print(f"Items found: {items}, actual wait: {elapsed:.2f}s")
    browser.close()
    

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(filepath)
    page.wait_for_selector("#spinner", state="hidden")

    items = page.locator(".feed-item").count()
    print("Items found:", items)
    browser.close()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(filepath)
    page.wait_for_load_state("networkidle")

    items = page.locator(".feed-item").count()
    print("Items found:", items)
    browser.close()
    

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(filepath)
    page.click("#load-more")

    page.wait_for_selector("text=Order #1045")
    items = page.locator(".feed-item").count()
    print("Items after clicking Load More:", items)
    browser.close()