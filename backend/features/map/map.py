from fastapi import APIRouter, FastAPI, HTTPException
import json

router= APIRouter(prefix='/map', tags=['map'])

with open('sri_lanka_places.json','r') as file:
    places= json.load(file)

@router.get('/')
def map(dest_name:str):
    for place in places:
        if place['name'].lower() == dest_name.lower():
            return place
        else:
            raise HTTPException(status_code=404, detail="Destination not found")
