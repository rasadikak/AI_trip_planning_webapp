from fastapi_mail import FastMail, ConnectionConfig, MessageSchema
from backend.config import settings
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends, APIRouter
from backend.login import database, orm_model
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

ACCESS_TOKEN_EXPIRE_MINUTES3=30
SECRET_KEY3= 'dsvhks438s'
ALGORITHM3='HS256'


router= APIRouter(prefix='/verify_mail')

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
    to_encode.update({"exp": expire_time})
    token= jwt.encode(to_encode, SECRET_KEY3, algorithm=ALGORITHM3)
    return token

def verify_token(token:str):
    try:
        payload =jwt.decode(token, SECRET_KEY3, algorithms=[ALGORITHM3])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=400, detail=f'invalid token')
        return user_id
    except jwt.ExpiredSignatureError:

        raise HTTPException(status_code=400, detail="Verification link expired")

    except JWTError:
          raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )   


async def send_mail(email:str, db:Session=Depends(database.get_db)):
    user= db.query(orm_model.User).filter(orm_model.User.email==email).first()
    if not user:
        raise HTTPException(status_code=400, detail=f'user dosnt exist')
    user_id= user.id
    token= create_token({"user_id": user_id})
    
    
    link=f"http://127.0.0.1:8000/verify_mail?token={token}"
    
    await send_email_verify_for_signup(email, link)
    return "verify link sent sucesfully"
    
@router.get('/')
def verify_mail(token: str,db:Session=Depends(database.get_db)):
  user_id= verify_token(token)
  user= db.query(orm_model.User).filter(orm_model.User.id==user_id).first()
  if not user:

        raise HTTPException(status_code=404, detail="User not found")
  user.is_verified = True

  db.commit()


  return RedirectResponse(url='/frontend/home/login.html', status_code=302, detail=f'user redirected succefully')