from fastapi import APIRouter, Form
from  dotenv import load_dotenv
import requests
import os
from backend.config import HF_TOKEN
from openai import OpenAI

load_dotenv()



url ="https://router.huggingface.co/v1"
model="meta-llama/Llama-3.1-8B-Instruct:novita"

router= APIRouter(prefix="/chatbot", tags=['chatbot'])

conversation_history=[]

messages=[]

system_prompt={
         "role": "system",
         "content": (
        "You are an AI travel assistant for Sri Lanka used in an AI Trip Planner web application. "
        "Your main responsibility is to answer users' questions about traveling in Sri Lanka. "
        
        "Provide clear, accurate, and concise information about:\n"
        "- Tourist destinations\n"
        "- Attractions and sightseeing\n"
        "- Culture and local experiences\n"
        "- Transportation options\n"
        "- Hotels and accommodation types\n"
        "- Food and restaurants\n"
        "- Travel tips and safety advice\n"
        
        "Rules you must follow:\n"
        "1. Answer the user's question directly and clearly.\n"
        "2. Do NOT generate full travel itineraries or trip plans unless the user explicitly asks for one.\n"
        "3. If the question is unrelated to travel in Sri Lanka (politics, global news, programming, etc.), "
        "politely say that you are designed to answer Sri Lanka travel-related questions only.\n"
        "4. If you are unsure or the question requires real-time or up-to-date information, say: "
        "'I’m sorry, I don’t have up-to-date information about that.' Do not guess or invent facts.\n"
        "5. Keep responses friendly, helpful, and easy to understand.\n"
        "6. Prefer short explanations (3–6 sentences) unless the user asks for more details."
    )
}

@router.post('/')
def chatbot(chatInput:str=Form(...)): 
    
    print(chatInput)

    conversation_history.append({
        "role": "user",
        "content": chatInput
        
    })

    messages = [system_prompt] + conversation_history

    client = OpenAI(
       base_url= url,
       api_key=HF_TOKEN
    )

    

    completion = client.chat.completions.create(
        model=model,
        messages=messages
       
    )

    response=completion.choices[0].message.content

    conversation_history.append({
        "role": "assistant",
        "content": response
    })

    
    
    
    print(response)
    return {"response": response}



#im using open ai Llama 3.1 8B Instruct model 