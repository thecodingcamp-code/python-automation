import requests
from bs4 import BeautifulSoup

response = requests.get("https://example.com/products.html")
print(response.status_code)
print(response.text[:200])

with open("products.html", "r") as f:
    html_content = f.read()
    


soup = BeautifulSoup(html_content, "html.parser")
print(soup.title.string)

product_cards = soup.find_all("div", class_="product-card")
print("Number of products found:", len(product_cards))

for card in product_cards:
    name = card.find("h2", class_="product-name").text
    price = card.find("span", class_="product-price").text
    desc = card.find("p", class_="product-desc").text
    print(f"{name} | {price} | {desc}")
    
products = []

for card in product_cards:
    products.append({
        "name": card.find("h2", class_="product-name").text,
        "price": card.find("span", class_="product-price").text,
        "description": card.find("p", class_="product-desc").text,
    })

print(products)

names = soup.select(".product-name")
for name in names:
    print(name.text)