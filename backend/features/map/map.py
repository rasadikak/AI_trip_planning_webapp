from fastapi import APIRouter, FastAPI, HTTPException
import json
import requests


url = "https://nominatim.openstreetmap.org/search"

router= APIRouter(prefix='/map', tags=['map'])

with open('backend/features/map/sri_lanka_places.json','r', encoding='utf-8') as file:
    #print("ok 1")
    places= json.load(file)
    #print("ok 1")

@router.get('/')
def map(dest_name:str):
    print(dest_name)
    for place in places:
        if place['name'].lower() == dest_name.lower():
            print(place)
            return place
        
    else:
         params={"q":dest_name, "format":"json","limit":1}   
         response= requests.get(url, params=params, headers={"User-Agent": "trip-app"})
         print(response.json())
         data=response.json()
         if data:
              place= data[0] #i added this because api may return list of results
              return {"name":place["name"], "lat":place["lat"] , "lon":place["lon"]}
         else:
              raise HTTPException(status_code=404, detail="Destination not found")
