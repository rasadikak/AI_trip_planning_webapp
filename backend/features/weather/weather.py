from fastapi import FastAPI,APIRouter, Form, HTTPException
from backend.config import WEATHER_API
import requests

router= APIRouter(prefix='/weather', tags=['weather'])



@router.post('/')
def weather_api(place:str=Form(...)):
    print("weather api loaded")
    try:
        print("try first")
        url= f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={place}"
        print(url)
        response= requests.get(url)
        print("response", response)
        data= response.json()
        print("data", data)
        if "error" in data:
            raise HTTPException(status_code=404, detail=f"destination not found")
        print(data)
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

