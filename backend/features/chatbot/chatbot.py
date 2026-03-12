from fastapi import APIRouter, Form
from  dotenv import load_dotenv
import requests
import os
from backend.config import HF_TOKEN
from openai import OpenAI

load_dotenv()



url ="https://router.huggingface.co/v1"
print(url)



model="meta-llama/Llama-3.1-8B-Instruct:novita"

router= APIRouter(prefix="/chatbot", tags=['chatbot'])

@router.post('/')
def chatbot(chatInput:str=Form(...)): 
    
    print(chatInput)

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
        "You are a helpful Sri Lanka travel assistant. "
        "Your responsibility is to answer users' questions clearly, accurately, and concisely. "
        "Provide information about destinations, local tips, culture, transport, hotels, and sightseeing. "
        "Do NOT generate full itineraries or plans unless explicitly asked. "
        "Always be friendly, polite, and informative."
    )
},
        {
            
            "role": "user",
            "content": chatInput
        }
    ],
)

    response=completion.choices[0].message.content
    print(response)
    return {"response": response}



#im using open ai Llama 3.1 8B Instruct model 