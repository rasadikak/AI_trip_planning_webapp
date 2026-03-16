from fastapi import APIRouter, Form
from  dotenv import load_dotenv
import requests
import os
from backend.config import HF_TOKEN
from openai import OpenAI
from typing import List

load_dotenv()



url ="https://router.huggingface.co/v1"
print(url)



model="meta-llama/Llama-3.1-8B-Instruct:novita"

router= APIRouter(prefix="/planner_api", tags=['planner_api'])

@router.post('/')
def trip_planner_api(destinationType:str= Form(...),
                    budget:str=Form(...),
                    numDays:int=Form(...) ,
                    numPeople:int=Form(...),accommodation:str=Form(...),
                    foodPreference:List[str]=Form([])): 
    
    print(foodPreference)
    food_pref_string= ", ".join(foodPreference)
    print(food_pref_string)

    question = f"""
You are a professional Sri Lanka travel planner ✈️🌴 specializing in creating detailed, realistic travel itineraries.

Trip Details:
- Destination Type(s): {destinationType} 🏖️🌄🏙️
- Budget Level: {budget} 💰
- Number of Days: {numDays} 📅
- Number of Travelers: {numPeople} 👥
- Accommodation Preference: {accommodation} 🏨🏠
- Food Preference: {food_pref_string} 🍽️

IMPORTANT RULES:
- Only suggest **REAL locations in Sri Lanka**.
- Do NOT invent fake cities, beaches, or restaurants.
- Prefer **well-known tourist destinations** and **popular local places**.
- All prices must be **approximate and written in Sri Lankan Rupees (LKR)**.
  Example: (Approx. 3000 LKR)
- Ensure the itinerary is **realistic for {numDays} days**.
- Activities should consider **travel distance and time**.

Instructions:

1️⃣ Suggest **2–3 alternative itineraries** so the traveler can choose.

2️⃣ Each itinerary should focus on **destinations that match the selected destination types**.

3️⃣ For each day include:

Morning 🌅  
- Activities with **specific attractions or beaches**

Afternoon ☀️  
- Activities such as sightseeing, markets, cultural sites, wildlife, or water sports

Evening 🌙  
- Relaxing activities such as sunset viewpoints, beach walks, nightlife, or cultural shows

4️⃣ Food Suggestions 🍽️  
Include:
- **Restaurant name**
- **Popular dish**
- Approximate price (LKR)

Example:
- **Dewmini Roti Shop – Mirissa**  
  Dish: Chocolate Banana Roti  
  Price: (Approx. 1200 LKR)

5️⃣ Accommodation Suggestions 🏨  
Include:
- **Hotel or guesthouse name**
- Area/location
- Approximate price range
- Google Maps link
- Official website if available

Example:
- **Paradise Beach Club – Mirissa**  
  📍 Mirissa Beach  
  💰 (Approx. 18,000 LKR per night)  
  🗺 Google Maps: https://maps.google.com/?q=Paradise+Beach+Club+Mirissa  
  🌐 Website: https://www.paradisebeachclub.lk

6️⃣ Add **transport suggestions** between destinations.

Example:
- Tuk-tuk (10 minutes)  
- Train from Colombo to Galle (2 hours)  
- Boat ride to whale watching area

7️⃣ Add **important travel tips** including:
- Safety tips
- Best time to visit attractions
- Local customs
- Transport advice
- Weather considerations
- Booking tips for hotels or tours

8️⃣ Use **structured Markdown formatting with headings, bullet points, and emojis** so it looks good in both web pages and PDFs.

Output Format:

## Itinerary 1 🗺️

### Trip Summary
Destination: [Main destination] 🌴  
Best For: [Beach / Nature / Adventure / Culture]

---

### Day 1 📅

Morning 🌅
- Activity

Afternoon ☀️
- Activity

Evening 🌙
- Activity

Food 🍽️
- Restaurant suggestion

Accommodation 🏨
- Hotel suggestion with links

---

### Day 2 📅
(Same structure)

---

### Travel Tips 💡
- Tip 1
- Tip 2
- Tip 3

---

## Itinerary 2 🗺️
(Same structure)

"""

    client = OpenAI(
       base_url= url,
       api_key=HF_TOKEN,
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
        {
    "role": "system",
    "content": (
        "You are an expert Sri Lanka travel planning assistant used in an AI Trip Planner web application. "
        "Your primary task is to generate detailed and realistic travel itineraries based on user inputs such as "
        "destination type, budget level, number of days, number of travelers, accommodation preference, and food preference.\n\n"

        "Your responsibilities:\n"
        "- Create well-structured travel itineraries for Sri Lanka.\n"
        "- Recommend real tourist destinations, attractions, restaurants, and accommodations.\n"
        "- Ensure the trip plan is realistic for the given number of days.\n"
        "- Consider travel time and distance between locations.\n"
        "- Provide practical suggestions for transportation, food, accommodation, and activities.\n\n"

        "Strict rules:\n"
        "1. Only suggest REAL locations in Sri Lanka. Never invent places.\n"
        "2. Ensure the plan matches the user's selected destination types (beach, hill country, wildlife, cultural, city, etc.).\n"
        "3. Prices must be approximate and written in Sri Lankan Rupees (LKR).\n"
        "4. Include restaurants with dishes and estimated prices.\n"
        "5. Include accommodation suggestions with approximate price ranges.\n"
        "6. Include transport suggestions between locations.\n"
        "7. Include useful travel tips such as safety, weather, and local customs.\n"
        "8. Format responses clearly using Markdown headings, bullet points, and emojis.\n\n"

        "Output requirements:\n"
        "- Generate 2–3 alternative trip itineraries.\n"
        "- Each itinerary must include daily activities for morning, afternoon, and evening.\n"
        "- Include food recommendations and accommodation suggestions.\n"
        "- Ensure the response is visually structured so it can be displayed on a website or exported to a PDF.\n\n"

        "Your goal is to create practical, enjoyable, and realistic Sri Lanka travel plans for tourists."
    )
},

        {
            
            "role": "user",
            "content": question
        }
    ],
)

    response=completion.choices[0].message.content
    print(response)
    return {"response": response}



#im using open ai Llama 3.1 8B Instruct model 