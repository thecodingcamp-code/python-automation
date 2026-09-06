from bs4 import BeautifulSoup
from lxml import html

with open("catalog.html") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

fragile = soup.select(".css-3f8a1")
print("Fragile selector match:", len(fragile))

cards = soup.select('[data-testid="product-card"]')
print("Cards found via data-testid:", len(cards))

featured = soup.select(".product-card.featured")
print(featured[0].find("h2").text)

course_links = soup.select('a[href^="/courses/"]')
print("Course links found:", len(course_links))

target = soup.select('.product-card:has(a[href="/courses/ai-engineering"])')
print(target[0].find("h2").text)


tree = html.fromstring(open("catalog.html").read())

next_links = tree.xpath('//a[text()="Next"]')
print("Exact matches:", len(next_links))
for link in next_links:
    print(link.text, "->", link.get("href"))
    
contains_next = tree.xpath('//*[contains(text(), "Next")]')
print("Contains matches:", len(contains_next))
for el in contains_next:
    print(el.tag, "-", el.text.strip()[:50])
    
price_el = tree.xpath('//span[text()="$179.00"]')[0]
parent_card = price_el.xpath("..")[0]
name = parent_card.xpath('.//h2[@class="product-name"]/text()')[0]
print(name)