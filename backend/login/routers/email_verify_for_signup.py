from fastapi_mail import FastMail, ConnectionConfig, MessageSchema
from backend.config import settings
from jose import jwt, JWTError
from datetime import datetime, timedelta

ACCESS_TOKEN_EXPIRE_MINUTES3=30
SECRET_KEY3= 'dsvhks438s'
ALGORITHM3='HS256'


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,  # your email
    MAIL_PASSWORD=settings.MAIL_PASSWORD,  # your email password / app password
    MAIL_FROM=settings.MAIL_FROM,          # sender email
    MAIL_PORT=settings.MAIL_PORT,          # port number (587 or 465)
    MAIL_SERVER=settings.MAIL_SERVER,      # smtp.gmail.com, etc.
    MAIL_STARTTLS=settings.MAIL_STARTTLS,            # True or False
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,            # True or False
    USE_CREDENTIALS=True                    # login required
)

async def send_email_verify_for_signup(email:str, link:str):
    message=MessageSchema(
        subject="Verify your email before signup",
        recipients=[email],
        body= f"""
         Click this link to verify your email:

        {link}

        This link expires in 30 minutes.
        """,
        subtype="plain"

    )
    fm= FastMail(conf)
    await fm.send_message(message)
 

def create_token(data:dict):
    to_encode= data.copy()
    expire_time= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES3)
    to_encode.update(expire_time)
    token= jwt.encode(to_encode, SECRET_KEY3, algorithm=ALGORITHM3)
    return token

  