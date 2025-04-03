import re
import time
import httpx
from fastapi import FastAPI, Query
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Function to clean text
def clean_text(text):
    return re.sub(r"\s+", " ", text.strip())

# Function to scrape FragranceNet
def scrape_fragrancenet(fragrance_name):
    base_url = "https://www.fragrancenet.com/cologne/"
    search_url = f"{base_url}{fragrance_name.replace(' ', '-').lower()}"

    # Use Selenium to handle JavaScript-loaded content
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(search_url)

    time.sleep(3)  # Wait for JavaScript to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    items = []

    # Find product listings
    for product in soup.find_all("div", class_="product-container"):
        price_elem = product.select_one("#pwcprice")  # Select using ID
        if price_elem:
            price = price_elem.text.strip()
        else:
            price = "Price not found"
        title_elem = product.find("h2", class_="product-title")
        link_elem = product.find("a", class_="product-image")

        if title_elem and price_elem and link_elem:
            title = clean_text(title_elem.text)
            price = clean_text(price_elem.text)
            link = "https://www.fragrancenet.com" + link_elem["href"]
            
            items.append({"title": title, "price": price, "link": link})

    return items if items else [{"error": "No products found"}]

# API Route
@app.get("/search")
async def search_cologne(q: str = Query(..., title="Fragrance Name")):
    results = scrape_fragrancenet(q)
    return {"results": results}
