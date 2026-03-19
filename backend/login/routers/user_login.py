from fastapi import FastAPI, APIRouter,Form, Depends, HTTPException
#from backend.main import app
from backend.login import orm_model, database,utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.login import oauth2
from fastapi.responses import RedirectResponse

router= APIRouter(prefix='/login', tags=['login'])

@router.post('/')
def login( user_credintials: OAuth2PasswordRequestForm = Depends(), db:Session= Depends(database.get_db)):
    print("before ok")
    user= db.query(orm_model.User).filter(orm_model.User.email==user_credintials.username).first()
    if not user:
         raise HTTPException(status_code= 400, detail=f'email not found')
    
    verify_pw= utils.verify(user_credintials.password, user.password)
    if  verify_pw== False :
            print("password wrong")
            raise HTTPException(status_code= 400, detail=f'wrong password') 
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    
    access_token= oauth2.create_token({"user_id":user.id})
    
    response= RedirectResponse(url=f'/frontend/features/trip_planner.html', status_code= 302) 
    response.set_cookie(key="access_token", value=f"bearer {access_token}", httponly=True)          
    #return {"access_token": access_token, "token_type":"bearer"}
    #response= RedirectResponse(url=f'/frontend/features/trip_planner.html', status_code= 302)
    #response.set_cookie(key="user_name", value=user.name)
    #response.set_cookie(key="user_email", value=user.email)
    return response
                  
           
    

   

