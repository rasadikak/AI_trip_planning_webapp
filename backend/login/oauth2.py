from jose import JWTError, jwt
#pip install python-jose[cryptography]
from backend.login import database, orm_model
from fastapi import Cookie
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from backend.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from sqlalchemy.orm import Session
from backend.logger import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#"Expect JWT token using OAuth2 Bearer Token method, and login endpoint is /login."


def create_token(data: dict):
    to_encode = data.copy()
    #print(to_encode)
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str):
    try:
        pay_load = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id  = pay_load.get("user_id")
        if user_id is None:
            logger.warning("Token verification failed — user_id missing in payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return user_id

    except JWTError:
        logger.warning("Token verification failed — invalid or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


def current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)
):
    try:
        token_data = verify_token(token)
        user_id    = verify_token(token)
        user       = db.query(orm_model.User).filter(orm_model.User.id == user_id).first()
        if not user:
            logger.warning(f"current_user — user not found id:{user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"current_user failed — error:{e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )


def current_user_cookie(
    access_token: str = Cookie(default=None),
    db: Session = Depends(database.get_db)
):
    if not access_token:
        logger.warning("current_user_cookie — no access token cookie found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in — no token cookie found"
        )

    try:
        # Remove "bearer " prefix that was added when setting the cookie
        token   = access_token.replace("bearer ", "")
        user_id = verify_token(token)
        user    = db.query(orm_model.User).filter(orm_model.User.id == user_id).first()

        if not user:
            logger.warning(f"current_user_cookie — user not found id:{user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"current_user_cookie failed — error:{e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )