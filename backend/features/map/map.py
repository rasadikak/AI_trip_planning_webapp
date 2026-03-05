from fastapi import APIRouter, FastAPI
import json

router= APIRouter(prefix='/map', tags=['map'])

with open('sri_lanka_places.json','r') as file:
    places= json.load(file)

@router.get('/')
def map(dest_name:str):

    print('map')
    return 'map'