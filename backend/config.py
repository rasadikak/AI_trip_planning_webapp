from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

load_dotenv()

SQLALCHEMY_DATABASE_URL= os.getenv("SQLALCHEMY_DATABASE_URL")
ACCESS_TOKEN_EXPIRE_MINUTES= os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM= os.getenv("ALGORITHM")
SECRET_KEY= os.getenv("SECRET_KEY")





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