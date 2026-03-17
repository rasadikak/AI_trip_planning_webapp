from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import json
import requests
import os

url = "https://nominatim.openstreetmap.org/search"

router= APIRouter(prefix='/map', tags=['map'])

# Setup Jinja2 templates
templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
templates = Jinja2Templates(directory=templates_dir)

with open('backend/features/map/sri_lanka_places.json','r', encoding='utf-8') as file:
    places= json.load(file)

def get_location_data(dest_name: str):
    """Fetch location data for a destination"""
    for place in places:
        if place['name'].lower() == dest_name.lower():
            return place
    
    # If not found locally, search via Nominatim API
    params = {"q": dest_name, "format": "json", "limit": 1}   
    response = requests.get(url, params=params, headers={"User-Agent": "trip-app"})
    data = response.json()
    if data:
        place = data[0]
        return {"name": place["name"], "lat": place["lat"], "lng": place["lon"]}
    
    return None

@router.get('/', response_class=HTMLResponse)
async def map(request: Request, dest_name: str):
    """Serve interactive map with the destination"""
    print(f"Map request for: {dest_name}")
    
    location = get_location_data(dest_name)
    
    if not location:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    # Prepare destinations list for template (single destination)
    destinations = [location]
    
    # Render template with location data
    return templates.TemplateResponse("map.html", {
        "request": request,
        "destinations": destinations,
        "initial_dest": location['name'],
        "initial_lat": location['lat'],
        "initial_lng": location['lng']
    })

@router.get('/json/')
def map_json(dest_name: str):
    """Return location data as JSON (for API/LLM agent use)"""
    print(f"Map JSON request for: {dest_name}")
    
    location = get_location_data(dest_name)
    
    if not location:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    return location
