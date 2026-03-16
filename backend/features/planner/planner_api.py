from fastapi import APIRouter, Form
from  dotenv import load_dotenv
import requests
import os
from backend.config import HF_TOKEN

from typing import List
from langchain_huggingface import HuggingFaceEndpoint
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_classic import hub
from langchain_core.tools import Tool
from langchain_huggingface import ChatHuggingFace
#from langchain.prompts import PromptTemplate

load_dotenv()

router= APIRouter(prefix="/planner_api", tags=['planner_api'])

url ="https://router.huggingface.co/v1"


base_llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    huggingfacehub_api_token=HF_TOKEN,
    temperature=0.7,
    max_new_tokens=2048,
    provider="novita" # Explicitly specifying the provider often helps
)
llm = ChatHuggingFace(llm=base_llm)
#template = """
#You are a professional Sri Lanka travel planner ✈️🌴.
#Plan realistic itineraries for the given trip request.
#Include **clickable map links** for every destination: http://localhost:8000/map/?dest_name=DESTINATION_NAME

#{input}
#"""

prompt = hub.pull("hwchase17/react")

def map(dest_name:str):
    map_url= "http://localhost:8000/map/"
    map_response= requests.get(map_url, params={"dest_name":dest_name})
    return map_response.json()

map_tool= Tool(
    name="map",
    func=map,
    description="use this tool to get directions  between  locations in Sri Lanka. Input should be a single city name"
)

tools= [map_tool]


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

5️⃣ Accommodation Suggestions 🏨  
Include:
- **Hotel or guesthouse name**
- Area/location
- Approximate price range
- Google Maps link
- Official website if available

6️⃣ For each **destination in the itinerary**, include a clickable **local map link** using this format:  
http://localhost:8000/map/?dest_name=DESTINATION_NAME

Example:
- Destination: Colombo
  Map: http://localhost:8000/map/?dest_name=Colombo

7️⃣ Add **transport suggestions** between destinations.

Example:
- Tuk-tuk (10 minutes)  
- Train from Colombo to Galle (2 hours)  
- Boat ride to whale watching area

8️⃣ Add **important travel tips** including:
- Safety tips
- Best time to visit attractions
- Local customs
- Transport advice
- Weather considerations
- Booking tips for hotels or tours

9️⃣ Use **structured Markdown formatting with headings, bullet points, and emojis** so it looks good in both web pages and PDFs.

Output Format:

## Itinerary 1 🗺️

### Trip Summary
Destination: [Main destination] 🌴  
Map: http://localhost:8000/map/?dest_name=[Main destination]  
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

Map Link for the destination: http://localhost:8000/map/?dest_name=[destination]

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
    
    

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    response = agent_executor.invoke({"input": question})
    return {"response":response}
    



#im using open ai Llama 3.1 8B Instruct model 