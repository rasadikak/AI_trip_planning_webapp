from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL= os.getenv("SQLALCHEMY_DATABASE_URL")
ACCESS_TOKEN_EXPIRE_MINUTES= os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM= os.getenv("ALGORITHM")
SECRET_KEY= os.getenv("SECRET_KEY")