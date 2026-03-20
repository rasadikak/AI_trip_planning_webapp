from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import json
import requests
import os

nominatim_url = "https://nominatim.openstreetmap.org/search"
router = APIRouter(prefix='/map', tags=['map'])

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
templates = Jinja2Templates(directory=templates_dir)

with open('backend/features/map/sri_lanka_places.json', 'r', encoding='utf-8') as file:
    places = json.load(file)


def get_location_data(dest_name: str):
    # Clean all variations of separators
    dest_name = dest_name.replace("_", " ").replace("-", " ").replace("+", " ").strip()

    # Check local JSON first
    for place in places:
        if place['name'].lower() == dest_name.lower():
            return place

    # Fallback to Nominatim with Sri Lanka context
    params = {
        "q": f"{dest_name} Sri Lanka",
        "format": "json",
        "limit": 1,
        "addressdetails": 1,
        "extratags": 1,
        "namedetails": 1
    }

    try:
        response = requests.get(
            nominatim_url,
            params=params,
            headers={"User-Agent": "serendib-trip-app"},
            timeout=5
        )
        data = response.json()

        if data:
            place = data[0]
            address = place.get("address", {})
            return {
                "name": dest_name,
                "lat": place["lat"],
                "lng": place["lon"],
                "display_name": place.get("display_name", dest_name),
                "type": place.get("type", ""),
                "city": address.get("city", address.get("town", "")),
                "district": address.get("state_district", ""),
                "province": address.get("state", "")
            }

    except Exception as e:
        print(f"Nominatim error for {dest_name}: {e}")

    return None


@router.get('/', response_class=HTMLResponse)
async def map_view(request: Request, dest_name: str):
    print(f"Map request for: {dest_name}")
    location = get_location_data(dest_name)
    if not location:
        raise HTTPException(status_code=404, detail="Destination not found")
    return templates.TemplateResponse("map.html", {
        "request": request,
        "destinations": [location],
        "initial_dest": location['name'],
        "initial_lat": location['lat'],
        "initial_lng": location['lng']
    })


@router.get('/json/')
def map_json(dest_name: str):
    print(f"Map JSON request for: {dest_name}")
    location = get_location_data(dest_name)
    if not location:
        raise HTTPException(status_code=404, detail="Destination not found")
    return location