from fastapi import APIRouter, Form
from  dotenv import load_dotenv
import requests
import os

load_dotenv()

DEEPSEEK_API_KEY= os.getenv("DEEPSEEK_API_KEY")
url = "https://api.deepseek.com/chat/completions"

headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}",
         "Content-Type":"application/json"}

router= APIRouter(prefix="/chatbot", tags=['chatbot'])

@router.post('/')
def chatbot(prompt:str=Form(...)):
    data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "You are a travel assistant for Sri Lanka."},
        {"role": "user", "content": prompt}
    ]
    }
    response= requests.post(url=url, json=data, headers=headers)
    response= response.json()
    print(response)
    return response