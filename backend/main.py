import logging
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from backend.login.routers import user_register,user_login, forget_password, signout, email_verify_for_signup,email_verify_for_login
from fastapi.staticfiles import StaticFiles
from backend.features.searchImage import search_img
from backend.features.map import map
from backend.features.pdf import pdf
from backend.features.profile import profile
#from backend.features.planner import planner

from backend.features.planner import planner_api
from backend.features.chatbot import chatbot
from backend.features.tripManagement import favDestination

app = FastAPI()
router = APIRouter(prefix="/test")





#It stops the "Instant Error" in the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"], # Allows your frontend to talk to your backend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
app.mount("/dataset", StaticFiles(directory="backend/features/searchImage/dataset"), name='dataset')
app.mount("/backend", StaticFiles(directory="backend"), name="backend")


app.include_router(user_register.router)
app.include_router(user_login.router)
app.include_router(forget_password.router)
app.include_router(email_verify_for_signup.router)
app.include_router(email_verify_for_login.router)
app.include_router(signout.router)

app.include_router(search_img.router)
app.include_router(map.router)
app.include_router(pdf.router)
app.include_router(profile.router)
#app.include_router(planner.router)
app.include_router(planner_api.router)
app.include_router(chatbot.router)
app.include_router(favDestination.router)

app.include_router(router)


