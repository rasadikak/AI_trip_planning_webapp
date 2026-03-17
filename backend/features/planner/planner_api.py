from fastapi import APIRouter, Form
from  dotenv import load_dotenv
import requests
import os
from backend.config import HF_TOKEN, WEATHER_API

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
    max_new_tokens=4096,
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




def weather(dest_name:str):
    clean_name = dest_name.split('\n')[0].replace('Observ', '').strip()
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={clean_name}"
    response = requests.get(url)
    return response.json()

weather_tool= Tool(
    name="weather",
    func=weather,
    description="Use this ONLY once per itinerary to verify the main city destination. input: destination name. Output: current weather data for that location (temperature, condition, etc.)"
)



def budget(transport:int, accommodation:int, food:int, activities:int):
    total= transport + accommodation + food + activities
    return f"Approximate total trip cost: {total} LKR"

budget_tool= Tool(
    name="budget",
    func=budget,
    description="Use this to calculate an approximate total trip cost in Sri Lankan Rupees (LKR) based on the costs of transport, accommodation, food, and activities. Input: transport cost, accommodation cost, food cost, activities cost (all in LKR)."
)
    

tools= [weather_tool, budget_tool]


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
You are a professional Sri Lanka travel planner ✈️🌴.

Create detailed, realistic travel itineraries based on the given trip details.

Trip Details:
- Destination Type(s): {destinationType}
- Budget Level: {budget}
- Number of Days: {numDays}
- Number of Travelers: {numPeople}
- Accommodation Preference: {accommodation}
- Food Preference: {food_pref_string}

----------------------------
IMPORTANT RULES
----------------------------
- Only suggest REAL locations in Sri Lanka 🇱🇰
- Do NOT invent fake places, hotels, or restaurants
- Keep plans realistic for {numDays} days
- All prices must be in LKR (Approximate)
- Consider travel time between locations

----------------------------
TOOL USAGE RULES
----------------------------
- Use the "weather" tool ONLY ONCE per itinerary to get current weather of the MAIN destination
- Use the "budget" tool to estimate total trip cost

----------------------------
INSTRUCTIONS
----------------------------

1. Generate EXACTLY 2 itineraries

2. Each itinerary must match the selected destination type(s)

3. For EACH DAY include:

Morning 🌅  
- Activities (specific places)

Afternoon ☀️  
- Activities (markets, sightseeing, nature, etc.)

Evening 🌙  
- Relaxing or cultural activities

4. Food 🍽️  
- Restaurant name  
- Popular dish  
- Approximate price (LKR)

5. Accommodation 🏨  
- Hotel name  
- Location  
- Price range  
- Google Maps link  
- Website (if available)

6. Map Links (IMPORTANT)  
For EVERY destination include:
http://localhost:8000/map/?dest_name=DESTINATION_NAME

7. Transport 🚗  
Mention travel method and time

8. Weather 🌦️  
- Use the weather tool and summarize the weather briefly

9. Budget 💰  
- Use the budget tool to estimate total cost

10. Travel Tips 💡  
- Safety  
- Best time to visit  
- Local customs  
- Transport advice  
- Booking tips  

----------------------------
OUTPUT FORMAT
----------------------------

Start with EXACTLY:

Final Answer:

Then:

## Itinerary 1 🗺️
(Full structured plan)

## Itinerary 2 🗺️
(Full structured plan)

----------------------------
IMPORTANT
----------------------------
- DO NOT include Thought, Action, Observation
- ONLY return clean Markdown
"""
    
    

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=25,
        max_execution_time=300,
        
    )
    response = agent_executor.invoke({"input": question})
    return {"response": response["output"]}
    



#im using open ai Llama 3.1 8B Instruct model 