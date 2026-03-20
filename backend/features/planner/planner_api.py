from fastapi import APIRouter, Form, HTTPException
import httpx
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
    provider="novita" 
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
    try:
        clean_name = dest_name.split('\n')[0].replace('Observ', '').strip()
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={clean_name}"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"Error fetching weather data for {dest_name}: {e}")
        return {"error": str(e)}

weather_tool= Tool(
    name="weather",
    func=weather,
    description="Use this ONLY once per itinerary to verify the main city destination. input: destination name. Output: current weather data for that location (temperature, condition, etc.)"
)




    

tools= [weather_tool]


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

Create a **detailed, realistic itinerary** based on the given trip details.

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
- Include **approximate costs in LKR** for:
  - Accommodation
  - Food
  - Activities
  - Transport
- Consider travel time between locations

----------------------------
TOOL USAGE RULES
----------------------------
- Use the **weather** tool **ONLY ONCE** for the main destination to summarize current weather

----------------------------
INSTRUCTIONS
----------------------------

1️⃣ Generate **exact 1  itinerary**.

2️⃣ Each day must include:

Morning 🌅  
- Activities (specific places) with approximate cost

Afternoon ☀️  
- Activities (markets, sightseeing, nature, cultural sites, etc.) with approximate cost

Evening 🌙  
- Relaxing or cultural activities with approximate cost

3️⃣ Food 🍽️  
- Restaurant name  
- Popular dish  
- Approximate price (LKR)

4️⃣ Accommodation 🏨  
- Hotel name  
- Location  
- Price range (per night in LKR)  
- Google Maps link  
- Website (if available)

5️⃣ Map Links 📍
----------------------------
STRICT RULE — THIS SECTION IS MANDATORY. YOU MUST INCLUDE IT EVERY TIME.
----------------------------
- You MUST add a section called "## Map Links 📍" at the END of the itinerary
- This section is NOT optional — always include it no matter what
- List the main geographic destinations ONLY (beaches, towns, parks, temples)
- Do NOT add map links inside activity descriptions
- Do NOT add map links for hotels, restaurants, or markets
- Use ONLY spaces in destination names — NO underscores, NO hyphens
- Do NOT add google maps links or any other links
- Every link MUST follow this EXACT format — do not change it:
  http://localhost:8000/map/?dest_name=DESTINATION NAME

EXAMPLE — copy this format exactly:

## Map Links 📍
- Mirissa Beach: http://localhost:8000/map/?dest_name=Mirissa 
- Weligama: http://localhost:8000/map/?dest_name=Weligama
- Galle Fort: http://localhost:8000/map/?dest_name=Galle 

MAXIMUM 5 links — only the most important geographic destinations.

WARNING: If you do not include this section with correct localhost links,
the response is considered incomplete and incorrect.

6️⃣ Transport 🚗  
- For **each segment between destinations**, provide **at least 2–3 travel options**:  
  - Bus, Train, Tuk-tuk, Taxi, or Boat (if applicable)  
  - Include **approximate cost** in LKR per person or per group  
  - Include **average travel time**  
  Example:
    - Bus from Colombo to Galle: 2.5 hours, ~LKR 150 per person  
    - Train from Colombo to Galle: 2 hours, ~LKR 200 per person  
    - Taxi from Colombo to Galle: 2 hours, ~LKR 3500 per car

7️⃣ Weather 🌦️  
- Use the weather tool to summarize the current weather briefly

8️⃣ Travel Tips 💡  
- Safety tips  
- Best time to visit attractions  
- Local customs  
- Transport advice  
- Booking tips

----------------------------
OUTPUT FORMAT
----------------------------

- Start the response **exactly** with:

Final Answer:

- Then provide the full itinerary in **clean, structured Markdown**, with headings, bullet points, and emojis.

----------------------------
IMPORTANT
----------------------------
- DO NOT include Thought, Action, Observation
- ONLY return clean Markdown
"""
    
    
    try:
        agent = create_react_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=25,
            max_execution_time=300
        
        )
        response = agent_executor.invoke({"input": question})
        return {"response": response["output"]}

    except httpx.ConnectError:
        # Network issue — can't reach HuggingFace API
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to AI service. Please check your internet connection and try again."
        )

    except httpx.TimeoutException:
        # Request took too long
        raise HTTPException(
            status_code=504,
            detail="AI service timed out. Please try again."
        )

    except TimeoutError:
        # Agent exceeded max_execution_time=300
        raise HTTPException(
            status_code=504,
            detail="Trip plan generation timed out. Try reducing the number of days."
        )

    except ValueError as e:
        # Bad input values
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )

    except KeyError as e:
        # response["output"] key missing
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected response from AI: {str(e)}"
        )

    except Exception as e:
        # Catch all other unexpected errors
        print(f"Unexpected error in trip_planner_api: {e}")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating your trip plan. Please try again."
        )

    


 