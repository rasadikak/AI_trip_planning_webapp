from langchain.agents import Tool,initialize_agent
from planner import planner_api
import requests
from fastapi import HTTPException

url= "http://127.0.0.1:8000/planner_api/"

response= requests.get(url)
if response.status_code==200:
    print("ok 1")
    llm_response= response.json()
else:
    raise HTTPException(status_code= response.status_code, detail=f"error calling planner_api {response.text}")



tools=[]

agent= initialize_agent(tools, planner_api, agent="zero-shot-react-description", verbose=True)
