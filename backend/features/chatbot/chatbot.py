import os
from fastapi import APIRouter, Form, Depends, HTTPException
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from google import genai

from backend.login import database, orm_model, oauth2
#from backend.login.routers import user_login
from backend.logger import logger

from backend.limiter_file import limiter
from fastapi import Request

load_dotenv()

router = APIRouter(prefix="/chatbot", tags=['chatbot'])

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

GEMINI_MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = (
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


@router.post('/')
@limiter.limit("10/minute")  # max 10 chat messages per minute
def chatbot(request: Request, db: Session = Depends(database.get_db), chatInput: str = Form(...), current_user=Depends(oauth2.current_user_cookie)):
    #print(current_user.id)

    # Basic sanitization
    chatInput = chatInput.strip()

    # Length limit — prevent extremely long inputs
    if len(chatInput) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Message too long. Please keep it under 1000 characters."
        )

    # Empty check
    if not chatInput:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    # Basic prompt injection detection
    suspicious_phrases = [
        "ignore previous instructions",
        "ignore your instructions",
        "forget your instructions",
        "you are now",
        "new instructions",
        "system prompt"
    ]

    if any(phrase in chatInput.lower() for phrase in suspicious_phrases):
        logger.warning(f"Possible prompt injection attempt — user:{current_user.id}")
        raise HTTPException(
            status_code=400,
            detail="Invalid message content"
        )
    try:
        logger.info(f"Chatbot request — user:{current_user.id}")

        db_history = db.query(orm_model.chatHistory).filter(orm_model.chatHistory.user_id == current_user.id).order_by(orm_model.chatHistory.created_at.asc()).limit(20).all()

        history_messages = [
            {"role": row.role, "content": row.content}
            for row in db_history   #converts rows of db query into a list of dictionaries with 'role' and 'content' keys
        ]

        logger.info(f"Chatbot input by user {current_user.id} — {chatInput}")

        # Convert stored history (role: user/assistant) into Gemini's expected format (role: user/model)
        gemini_history = []
        for msg in history_messages:
            role = "model" if msg["role"] == "assistant" else "user"
            gemini_history.append({"role": role, "parts": [{"text": msg["content"]}]})

        chat = client.chats.create(
            model=GEMINI_MODEL,
            config={"system_instruction": SYSTEM_PROMPT},
            history=gemini_history
        )

        gemini_response = chat.send_message(chatInput)

        response = gemini_response.text

        user_content = orm_model.chatHistory(user_id=current_user.id, role="user", content=chatInput)
        assistant_content = orm_model.chatHistory(user_id=current_user.id, role="assistant", content=response)
        db.add(user_content)
        db.add(assistant_content)
        db.commit()

        logger.info(f"Chatbot response sent — user:{current_user.id}")
        return {"response": response}

    except Exception as e:
        logger.critical(f"Chatbot crashed: {e} — user:{current_user.id}")
        raise HTTPException(status_code=500, detail="Something went wrong")


#im using gemini-2.5-flash model