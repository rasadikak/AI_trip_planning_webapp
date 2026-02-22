from fastapi import FastAPI, APIRouter,status, Form, HTTPException, Depends
import re
from backend.login import database, orm_model, schemas
from sqlalchemy.orm import Session
from backend.login import utils
from typing import List
from fastapi.responses import JSONResponse



router= APIRouter(prefix='/register', tags=['register'])



@router.get('/test')
def msg():
    print("fff")
    return 'bye'


def validate_user(name: str= Form(...), email: str= Form(...),password: str= Form(...),confirm_password: str= Form(...),db:Session=Depends(database.get_db)):
    if password!= confirm_password:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail=f'passwords do not match')
    if not re.fullmatch(r"[A-Za-z ]{3,}", name):
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Name must be at least 3 characters and contain only letters and spaces" )

    
    if not re.fullmatch(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid email address")
    
    existing_email= db.query(orm_model.User).filter(orm_model.User.email==email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'{email} exists')
   
    if not re.fullmatch(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$", password):
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters long and include uppercase, lowercase, number, and special character" )
    
    if len(password) > 64:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail= f"Password too long (max 64 characters)")

    return {"name": name, "email": email, "password": password}


@router.post('/', status_code= status.HTTP_200_OK, response_model= schemas.UserResponse)
def create_user(db:Session=Depends(database.get_db),user=Depends(validate_user)):
    print("before")
    hashed_pw= utils.hash(user['password'])
    print("pw hashed suucessfully")
    new_user= orm_model.User(name=user['name'], email=user['email'],password=hashed_pw)
    print("new user cretaed successfully")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print("after")
    return new_user
    
    


#  email verification
@router.get('/admin',response_model= List[schemas.UserResponse])
def get_all(db:Session=Depends(database.get_db)):
    users= db.query(orm_model.User).all()
    return users

@router.get('/admin/{id}', response_model=schemas.UserResponse)
def get_user(id:int , db:Session=Depends(database.get_db)):
    user= db.query(orm_model.User).filter(orm_model.User.id==id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'user {id} does not exist')
    return user
    
    
@router.delete('/delete/{id}')
def delete_user(id:int, db:Session=Depends(database.get_db)):
    user= db.query(orm_model.User).filter(orm_model.User.id==id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'user {id} does not exist')
    db.delete(user)
    db.commit()
    return JSONResponse(status.HTTP_204_NO_CONTENT, detail=f'user {id}  deleted')