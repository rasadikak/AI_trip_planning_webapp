from fastapi import APIRouter, Form, HTTPException
import httpx

from backend.limiter_file import limiter
from fastapi import Request

import requests

from backend.config import HF_TOKEN #WEATHER_API
from backend.logger import logger

from typing import List
from langchain_huggingface import HuggingFaceEndpoint
from langchain_classic.agents import AgentExecutor, create_react_agent
#from langchain_classic import hub
from langchain_core.tools import Tool
from langchain_huggingface import ChatHuggingFace
#from langchain.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate



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

#prompt = hub.pull("hwchase17/react", dangerously_pull_public_prompt=True)
prompt = PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}""")




def weather(dest_name:str):
    try:
        clean_name = dest_name.split('\n')[0].replace('Observ', '').strip()
        url = f"https://wttr.in/{clean_name}?format=j1"

        #url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={clean_name}"
        #old api based weather tool
        response = requests.get(url)
        return response.json()
    except Exception as e:
        #print(f"Error fetching weather data for {dest_name}: {e}")
        logger.warning(f"Weather tool failed for {dest_name}: {e}")
        return {"error": str(e)}

weather_tool= Tool(
    name="weather",
    func=weather,
    description="Use this ONLY once per itinerary to verify the main city destination. input: destination name. Output: current weather data for that location (temperature, condition, etc.)"
)




    

tools= [weather_tool]


@router.post('/')
@limiter.limit("3/minute")  # max 3 trip plans per minute per user
def trip_planner_api(request: Request,
                    destinationType:str= Form(...),
                    budget:str=Form(...),
                    numDays:int=Form(...) ,
                    numPeople:int=Form(...),accommodation:str=Form(...),
                    foodPreference:List[str]=Form([])): 
    

    if numDays < 1 or numDays > 30:
        raise HTTPException(status_code=400, detail="Number of days must be between 1 and 30")

    if numPeople < 1 or numPeople > 20:
        raise HTTPException(status_code=400, detail="Number of people must be between 1 and 20")

    valid_destinations = ["beach", "upcountry", "city", "safari", "culturel"]
    if destinationType not in valid_destinations:
        raise HTTPException(status_code=400, detail="Invalid destination type")

    valid_budgets = ["low", "mid", "high"]
    if budget not in valid_budgets:
        raise HTTPException(status_code=400, detail="Invalid budget type")

    valid_accommodations = ["hotel", "tents", "five_star", "kabana"]
    if accommodation not in valid_accommodations:
        raise HTTPException(status_code=400, detail="Invalid accommodation type")
    
    #print(foodPreference)
    food_pref_string= ", ".join(foodPreference)
    #print(food_pref_string)
    logger.info(f"Plan requested — type:{destinationType} days:{numDays} people:{numPeople} budget:{budget}")

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
- At the END of the itinerary add ONE section called "## Map Links 📍"
- Generate a real Google Maps search link for each destination
- Format EXACTLY like this:

## Map Links 📍
- Galle Fort: https://www.google.com/maps/search/Galle+Fort+Sri+Lanka
- Hikkaduwa Beach: https://www.google.com/maps/search/Hikkaduwa+Beach+Sri+Lanka
- Mirissa: https://www.google.com/maps/search/Mirissa+Sri+Lanka

RULES:
- ONLY geographic destinations — beaches, towns, parks, landmarks
- NO hotels, restaurants, markets, or museums
- Replace spaces with + in the URL
- Always add +Sri+Lanka at the end
- MAXIMUM 5 links

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
        logger.info(f"Plan generated successfully — type:{destinationType} days:{numDays}")
        return {"response": response["output"]}

    except httpx.ConnectError:
        # Network issue — can't reach HuggingFace API
        logger.error(f"HuggingFace unreachable — type:{destinationType} days:{numDays}")
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to AI service. Please check your internet connection and try again."
        )

    except httpx.TimeoutException:
        # Request took too long
        logger.error(f"HuggingFace timeout — type:{destinationType} days:{numDays}")
        raise HTTPException(
            status_code=504,
            detail="AI service timed out. Please try again."
        )

    except TimeoutError:
        # Agent exceeded max_execution_time=300
        logger.warning(f"Plan generation timed out — days:{numDays}")
        raise HTTPException(
            status_code=504,
            detail="Trip plan generation timed out. Try reducing the number of days."
        )

    except ValueError as e:
        # Bad input values
        logger.warning(f"ValueError in planner: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Network connection error, try again later"
        )

    except KeyError as e:
        # response["output"] key missing
        logger.error(f"KeyError in planner — missing key: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected response from AI: {str(e)}"
        )

    except Exception as e:
        # Catch all other unexpected errors
        #print(f"Unexpected error in trip_planner_api: {e}")
        logger.critical(f"Planner crashed: {e} — type:{destinationType} days:{numDays}")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating your trip plan. Please try again."
        )



    #pip install huggingface-hub
    #pip install langchain_huggingface
    #pip install langchain_classic