import logging
from fastapi import FastAPI, APIRouter
from backend.login.routers import user_register,user_login, forget_password, signout
from fastapi.staticfiles import StaticFiles

app = FastAPI()
router = APIRouter(prefix="/test")

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


app.include_router(user_register.router)
app.include_router(user_login.router)
app.include_router(forget_password.router)
app.include_router(signout.router)
app.include_router(router)


