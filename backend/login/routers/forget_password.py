from fastapi import APIRouter, Depends, HTTPException,Form, Response
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from backend.login import database,orm_model,utils
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from backend.login.routers.send_reset_email import send_reset_email
from backend.config import ALGORITHM2, SECRET_KEY2, ACCESS_TOKEN_EXPIRE_TIME2

router= APIRouter(prefix='/reset_pw')



def create_token(data:dict):
    to_encode= data.copy()
    expire_time= datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_TIME2)
    to_encode.update({"exp":expire_time})
    token= jwt.encode(to_encode,  SECRET_KEY2, algorithm=ALGORITHM2)
    return token

@router.post('/request_reset')
async def request_reset(email:str =Form(...),db:Session=Depends(database.get_db)):
    print("hi")
    user= db.query(orm_model.User).filter(orm_model.User.email==email).first()
    if not user:
        raise HTTPException(status_code= 404, detail=f'user does not exist in db')
    if user:
        print("user exists")
        token= create_token({"user_id": user.id})
        print({"token":token})
        reset_link=f"http://127.0.0.1:8000/reset_pw/reset_link?token={token}"
        await send_reset_email(email, reset_link)

        return {"msg": "Password reset email sent successfully"}



@router.get('/reset_link')
def reset_link():
    return RedirectResponse(url='/frontend/home/password_forget.html', status_code= 302)
#opens the html page for reset








@router.post('/forget_pw')
def forget_password(email:str=Form(...), new_password:str=Form(...),confirm_new_pw:str=Form(...) ,db:Session= Depends(database.get_db)):
    #print(email)
    #print(new_password)
    #print(confirm_new_pw)
    
    
    user= db.query(orm_model.User).filter(orm_model.User.email==email).first()
    if not user:
        raise HTTPException(status_code=404, detail=f'user does not exist in db')
    if user:
         if new_password== confirm_new_pw:
             
         
             hashed_pw= utils.hash(new_password)
             
             user.password= hashed_pw
             
             
             db.commit()
             db.refresh(user)
             print("congratssss")
         else:    
         
            raise HTTPException(status_code=400, detail=f'passwords are not similar')