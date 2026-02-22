from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

load_dotenv()

SQLALCHEMY_DATABASE_URL= os.getenv("SQLALCHEMY_DATABASE_URL")

#for login
ACCESS_TOKEN_EXPIRE_MINUTES= os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM= os.getenv("ALGORITHM")
SECRET_KEY= os.getenv("SECRET_KEY")

#fo reset password
ALGORITHM2=os.getenv("ALGORITHM2")
SECRET_KEY2=os.getenv("SECRET_KEY2")
ACCESS_TOKEN_EXPIRE_TIME2=os.getenv("ACCESS_TOKEN_EXPIRE_TIME2")



class Settings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    class Config:
        env_file = ".env"

settings = Settings()