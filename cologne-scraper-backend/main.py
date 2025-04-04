import time
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape_fragrancenet

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Route
@app.get("/search")
async def search_cologne(q: str = Query(..., title="Fragrance Name")):
    results = scrape_fragrancenet(q)
    return {"results": results}
