from fastapi import FastAPI, APIRouter,Form, Depends, HTTPException
#from backend.main import app
from backend.login import orm_model, database,utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.login import oauth2

router= APIRouter(prefix='/login', tags=['login'])

@router.post('/')
def login( user_credintials: OAuth2PasswordRequestForm = Depends(), db:Session= Depends(database.get_db)):
    print("before ok")
    user= db.query(orm_model.User).filter(user_credintials.username==orm_model.User.email).first()
    if not user:
         raise HTTPException(status_code= 400, detail=f'email not found')
    
    verify_pw= utils.verify(user_credintials.password, user.password)
    if  verify_pw== False :
            print("password wrong")
            raise HTTPException(status_code= 400, detail=f'wrong password') 
    
    if user:
          if verify_pw == True:
                access_token= oauth2.create_token({"user_id":user.id})
                
                return {"access_token": access_token, "token_type":"bearer"}
         
           
    

   

