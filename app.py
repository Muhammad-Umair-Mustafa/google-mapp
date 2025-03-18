from fastapi import FastAPI, HTTPException, Query
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI()

GOOGLE_MAPS_BASE_URL = "https://www.google.com/maps/place/?q=place_id:{}"

# Function to extract Place ID from Google Maps URL
def extract_place_id(map_url: str) -> str:
    match = re.search(r'!3d([-\d.]+)!4d([-\d.]+)', map_url)
    if not match:
        raise HTTPException(status_code=400, detail="Invalid Google Maps URL")
    return match.group(0)  # Extracted Place ID

@app.get("/scrape")
def scrape_website(map_url: str = Query(..., title="Google Maps URL")):
    try:
        place_id = extract_place_id(map_url)
        url = GOOGLE_MAPS_BASE_URL.format(place_id)
        headers = {"User-Agent": "Mozilla/5.0"}
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch Google Maps page")
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract business website URL (may need adjustment based on Google's structure)
        website_tag = soup.find("a", string="Website")
        if not website_tag:
            raise HTTPException(status_code=404, detail="Website not found")
        
        website_url = website_tag.get("href")
        return {"map_url": map_url, "website": website_url}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
