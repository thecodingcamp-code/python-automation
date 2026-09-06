from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os

start_url = "file://" + os.path.abspath("page1.html")
all_products = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(start_url)

    page_num = 1
    while True:
        print(f"Scraping page {page_num}: {page.url}")
        soup = BeautifulSoup(page.content(), "html.parser")
        cards = soup.find_all("div", class_="product-card")

        for card in cards:
            all_products.append({
                "name": card.find("h2").text,
                "price": card.find("span").text,
            })

        next_link = page.query_selector("#next-link")
        if next_link is None:
            print("No next link found -- reached the last page")
            break

        next_link.click()
        page.wait_for_load_state("load")
        page_num += 1

    browser.close()

print()
print("Total products collected:", len(all_products))
