from jose import JWTError, jwt
from backend.login import  database, orm_model
from fastapi import Cookie
from fastapi import Depends, HTTPException,status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from backend.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from sqlalchemy.orm import Session



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#“Expect JWT token using OAuth2 Bearer Token method, and login endpoint is /login.”

def create_token(data:dict):
    to_encode = data.copy()
    print(to_encode)
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire_time})
    token= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token:str):
    try:
        pay_load= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id= pay_load.get("user_id")
        if user_id is None:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return user_id
    
    except JWTError:
          raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )   
    

def current_user( token:str=Depends(oauth2_scheme), db:Session= Depends(database.get_db)):
    token_data= verify_token(token)
    user_id= verify_token(token)
    user= db.query(orm_model.User).filter(orm_model.User.id== user_id).first()
    if not user:
          raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user




def current_user_cookie(
    access_token: str = Cookie(default=None),
    db: Session = Depends(database.get_db)
):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in — no token cookie found"
        )
    
    # Remove "bearer " prefix that was added when setting the cookie
    token = access_token.replace("bearer ", "")
    
    user_id = verify_token(token)
    
    user = db.query(orm_model.User).filter(orm_model.User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user



    
