from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

with open("dynamic_catalog.html") as f:
    raw_html = f.read()

soup = BeautifulSoup(raw_html, "html.parser")
product_cards = soup.find_all("div", class_="product-card")
print("Product cards found:", len(product_cards))
print("What we got instead:", soup.find("div", id="product-list").text.strip())


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("file://" + "/path/to/dynamic_catalog.html")

    immediate_text = page.inner_text("#product-list")
    print("Immediately after goto:", immediate_text)

    browser.close()
    
page.wait_for_selector(".product-card")

html_after = page.content()
soup = BeautifulSoup(html_after, "html.parser")
cards = soup.find_all("div", class_="product-card")

print("Product cards found:", len(cards))
for card in cards:
    print(card.find("h2").text, "-", card.find("span").text)
    
page.screenshot(path="rendered_page.png")