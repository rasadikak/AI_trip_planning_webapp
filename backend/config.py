from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

load_dotenv()

SQLALCHEMY_DATABASE_URL= os.getenv("SQLALCHEMY_DATABASE_URL")

#for login
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ALGORITHM= os.getenv("ALGORITHM")
SECRET_KEY= os.getenv("SECRET_KEY")

#fo reset password
ALGORITHM2=os.getenv("ALGORITHM2")
SECRET_KEY2=os.getenv("SECRET_KEY2")
ACCESS_TOKEN_EXPIRE_TIME2=int(os.getenv("ACCESS_TOKEN_EXPIRE_TIME2", "15"))

#for email verification

ALGORITHM3=os.getenv("ALGORITHM3")
SECRET_KEY3=os.getenv("SECRET_KEY3")
ACCESS_TOKEN_EXPIRE_MINUTES3=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES3", "30"))

HF_TOKEN=os.getenv("HF_TOKEN")

WEATHER_API=os.getenv("WEATHER_API")

class Settings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
     # Login JWT
    SQLALCHEMY_DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    SECRET_KEY: str

    # Reset password JWT
    ALGORITHM2: str
    SECRET_KEY2: str
    ACCESS_TOKEN_EXPIRE_TIME2: int

    #email verification jwt
    ALGORITHM3: str
    SECRET_KEY3: str
    ACCESS_TOKEN_EXPIRE_MINUTES3: int

    HF_TOKEN:str

    WEATHER_API:str

    class Config:
        env_file = ".env"

settings = Settings()