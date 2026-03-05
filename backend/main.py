import logging
from fastapi import FastAPI, APIRouter
from backend.login.routers import user_register,user_login, forget_password, signout, email_verify_for_signup,email_verify_for_login
from fastapi.staticfiles import StaticFiles
from backend.features.img_search import search_img
from backend.features.map import map

app = FastAPI()
router = APIRouter(prefix="/test")

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
app.mount("/dataset", StaticFiles(directory="backend/features/img_search/dataset"), name='dataset')
app.mount("/backend", StaticFiles(directory="backend"), name="backend")
app.mount("/static", StaticFiles(directory="backend/features/map/static"), name="static")

app.include_router(user_register.router)
app.include_router(user_login.router)
app.include_router(forget_password.router)
app.include_router(email_verify_for_signup.router)
app.include_router(email_verify_for_login.router)
app.include_router(signout.router)

app.include_router(search_img.router)
app.include_router(map.router)
app.include_router(router)


