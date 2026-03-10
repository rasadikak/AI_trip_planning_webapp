from fastapi import APIRouter,Form

from typing import List

import ollama

client= ollama.Client()

model= "deepseek-r1:1.5b"










router= APIRouter(prefix='/trip_planner', tags=['trip_planner'])

@router.post('/')
def trip_planner(destinationType:str= Form(...),
                    budget:str=Form(...),
                    numDays:int=Form(...) ,
                    numPeople:int=Form(...),accommodation:str=Form(...),
                    foodPreference:List[str]=Form([])):
    
    print(foodPreference)
    food_pref_string= ", ".join(foodPreference)
    print(food_pref_string)
    
    question = f"""
You are an expert Sri Lanka travel planner ✈️🌴.

Trip Details:
- Destination Type(s): {destinationType} 🏖️🌄🏙️
- Budget Level: {budget} 💰
- Number of Days: {numDays} 📅
- Number of Travelers: {numPeople} 👥
- Accommodation Preference: {accommodation} 🏨🏠
- Food Preference: {food_pref_string} 🍽️

Instructions:
1️⃣ Suggest multiple destinations in Sri Lanka matching the selected destination types.
2️⃣ Create 2–3 alternative itineraries for the trip (so the user can choose).
3️⃣ For each day in each itinerary:
   • Include activities with **specific locations**.
   • Include food suggestions with **restaurant names and dishes**.
   • Include accommodation suggestions with **specific hotel names or areas**.
4️⃣ Include **important travel tips**: safety, local customs, transport, peak times.
5️⃣ Make the plan realistic for {numPeople} travelers.
6️⃣ Output in a structured Markdown format, using emojis for readability.

Output Example:

## Itinerary 1 🗺️
### Trip Summary
Destination: Mirissa, Southern Coast 🏖️

### Day 1 📅
- Activities:
- Food:
- Accommodation:

### Day 2 📅
- Activities:
- Food:
- Accommodation:

Travel Tips 💡
- Tip 1
- Tip 2

---

## Itinerary 2 🗺️
...
"""
    response= client.generate(model=model, prompt=question)
    reply= response.response
    print(reply)
    return {"trip_plan":reply}