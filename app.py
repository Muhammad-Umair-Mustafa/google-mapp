from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI()

GOOGLE_MAPS_URL = "https://www.google.com/maps/place/?q=place_id:{}"

@app.get("/scrape")
def scrape_website(place_id: str):
    url = GOOGLE_MAPS_URL.format(place_id)
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch Google Maps page")
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract business website URL (may need adjustment based on Google's structure)
        website_tag = soup.find("a", string="Website")
        if not website_tag:
            raise HTTPException(status_code=404, detail="Website not found")
        
        website_url = website_tag.get("href")
        return {"place_id": place_id, "website": website_url}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
