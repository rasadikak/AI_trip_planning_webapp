from fastapi import FastAPI,APIRouter, Form, HTTPException
#from backend.config import WEATHER_API
import requests

router= APIRouter(prefix='/weather', tags=['weather'])



@router.post('/')
def weather_api(place:str=Form(...)):
    #print("weather api loaded")
    try:
        #print("try first")
        url= f"https://wttr.in/{place}?format=j1"
        #print(url)
        response = requests.get(url, timeout=20, headers={"User-Agent": "serendib-trip-app"})
        #print("response", response)
        #print("status:", response.status_code)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Destination not found")
        data= response.json()
        #print("keys:", list(data.keys()))
        current = data["current_condition"][0]
        
        nearest  = data.get("nearest_area", [{}])[0]
        location = nearest.get("areaName",  [{"value": place}])[0]["value"]
        region   = nearest.get("region",    [{"value": "Sri Lanka"}])[0]["value"]

        return {
            "location"  : location,
            "region"    : region,
            "temp_c"    : current["temp_C"],
            "feels_like": current["FeelsLikeC"],
            "condition" : current["weatherDesc"][0]["value"].strip(),
            "humidity"  : current["humidity"],
            "wind_kph"  : current["windspeedKmph"],
            "visibility": current["visibility"],
            "uv_index"  : current["uvIndex"]
        }

    except HTTPException:
        raise
    except KeyError as e:
        #print(f"Missing key: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected data format: {e}")
    except Exception as e:
        #print(f"Weather error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

