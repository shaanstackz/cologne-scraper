import re
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from selectors import fragrancenet_selectors

# Function to clean text
def clean_text(text):
    return re.sub(r"\s+", " ", text.strip())

# Function to scrape FragranceNet
def scrape_fragrancenet(fragrance_name):
    base_url = "https://www.fragrancenet.com/cologne/"
    search_url = f"{base_url}{fragrance_name.replace(' ', '-').lower()}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url, timeout=10000)

        # Wait for JavaScript to load
        page.wait_for_selector(fragrancenet_selectors["product_container"], timeout=5000)

        soup = BeautifulSoup(page.content(), "html.parser")
        browser.close()

    items = []

    # Find product listings
    for product in soup.select(fragrancenet_selectors["product_container"]):
        price_elem = product.select_one(fragrancenet_selectors["price"])
        title_elem = product.select_one(fragrancenet_selectors["title"])
        link_elem = product.select_one(fragrancenet_selectors["link"])

        if title_elem and price_elem and link_elem:
            title = clean_text(title_elem.text)
            price = clean_text(price_elem.text)
            link = "https://www.fragrancenet.com" + link_elem["href"]
            
            items.append({"title": title, "price": price, "link": link})

    return items if items else [{"error": "No products found"}]
