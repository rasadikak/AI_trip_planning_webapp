from fastapi import APIRouter, Form, Depends
from  dotenv import load_dotenv
from sqlalchemy.orm import Session
import requests
import os
from backend.config import HF_TOKEN
from openai import OpenAI
from backend.login import database,orm_model, oauth2
from backend.login.routers import user_login

load_dotenv()



url ="https://router.huggingface.co/v1"
model="meta-llama/Llama-3.1-8B-Instruct:novita"

router= APIRouter(prefix="/chatbot", tags=['chatbot'])



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
def chatbot(db:Session=Depends((database.get_db)),chatInput:str=Form(...),  current_user =Depends(oauth2.get_current_user)): 
    

    db_history=db.query(orm_model.chatHistory).filter(orm_model.chatHistory.user_id==current_user.id).order_by(orm_model.chatHistory.created_at.asc()).limit(20).all()
    
    history_messages = [
        {"role": row.role, "content": row.content}
        for row in db_history   #converts rows of db query into a list of dictionaries with 'role' and 'content' keys
    ]

    print(chatInput)

    history_messages.append({
        "role": "user",
        "content": chatInput
    })

   

    messages = [system_prompt] + history_messages
    

    client = OpenAI(
       base_url= url,
       api_key=HF_TOKEN
    )

    

    completion = client.chat.completions.create(
        model=model,
        messages=messages
       
    )

    response=completion.choices[0].message.content

    

    user_content=orm_model.chatHistory(user_id= current_user.id, role="user", content=chatInput)
    assistant_content=orm_model.chatHistory(user_id= current_user.id, role="assistant", content=response)
    db.add(user_content)
    db.add(assistant_content)
    db.commit()
    
    
    
    print(response)
    return {"response": response}



#im using open ai Llama 3.1 8B Instruct model 