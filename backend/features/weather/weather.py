from fastapi import FastAPI,APIRouter, Form, HTTPException
from backend.config import WEATHER_API
import requests

router= APIRouter(prefix='/weather', tags=['weather'])



@router.post('/')
def weather_api(place:str=Form(...)):
    try:
        url= "http://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={place}"
        response= requests.get(url)
        data= response.json()
        if "error" in data:
            return HTTPException(status_code=404, detail=f"destination not found")
        return {
            "location": data["location"]["name"],
            "region": data["location"]["region"],
            "temp_c": data["current"]["temp_c"],
            "feels_like": data["current"]["feelslike_c"],
            "condition": data["current"]["condition"]["text"],
            "icon": data["current"]["condition"]["icon"],
            "humidity": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"],
            "uv_index": data["current"]["uv"],
            "visibility": data["current"]["vis_km"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

