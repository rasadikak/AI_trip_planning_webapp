from fastapi import APIRouter, Depends, HTTPException, Form, Response
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from backend.login import database, orm_model, utils
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from backend.login.routers.send_reset_email import send_reset_email
from backend.config import ALGORITHM2, SECRET_KEY2, ACCESS_TOKEN_EXPIRE_TIME2, BASE_URL
from backend.logger import logger

router = APIRouter(prefix='/reset_pw')


def create_token(data: dict):
    to_encode  = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME2)
    to_encode.update({"exp": expire_time})
    token = jwt.encode(to_encode, SECRET_KEY2, algorithm=ALGORITHM2)
    return token


def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY2, algorithms=[ALGORITHM2])
        user_id = payload.get("user_id")
        if not user_id:
            logger.warning("Reset token invalid — user_id missing in payload")
            raise HTTPException(400, "Invalid token")
        return user_id
    except JWTError:
        logger.warning("Reset token expired or invalid")
        raise HTTPException(400, "Token expired or invalid")


@router.post('/request_reset')
async def request_reset(
    email: str = Form(...),
    db: Session = Depends(database.get_db)
):
    #print("hi")
    logger.info(f"Password reset requested — email:{email}")
    try:
        user = db.query(orm_model.User).filter(orm_model.User.email == email).first()

        if not user:
            logger.warning(f"Reset failed — user not found: {email}")
            raise HTTPException(status_code=404, detail=f'user does not exist in db')

        if user:
            #print("user exists")
            token      = create_token({"user_id": user.id})
            #print({"token":token})
            reset_link = f"{BASE_URL}/reset_pw/reset_link?token={token}"
            await send_reset_email(email, reset_link)
            logger.info(f"Password reset email sent — email:{email}")
            return {"msg": "Password reset email sent successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password reset request failed — email:{email} error:{e}")
        raise HTTPException(status_code=500, detail="Failed to send reset email")


@router.get('/reset_link')
def reset_link(token):
    logger.info("Reset link clicked — verifying token")
    try:
        verify_token = verify_reset_token(token)
        if verify_token:
            logger.info("Reset token valid — redirecting to reset page")
            return RedirectResponse(
                url=f'/frontend/home/password_forget.html?token={token}',
                status_code=302
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Reset link verification failed — error:{e}")
        raise HTTPException(status_code=500, detail="Reset link verification failed")
    #opens the html page for reset


@router.post('/forget_pw')
def forget_password(
    token: str = Form(...),
    new_password: str = Form(...),
    confirm_new_pw: str = Form(...),
    db: Session = Depends(database.get_db)
):
    #print(email)
    #print(new_password)
    #print(confirm_new_pw)
    logger.info("Password reset submission received")
    try:
        user_id = verify_reset_token(token)
        user    = db.query(orm_model.User).filter(orm_model.User.id == user_id).first()

        if not user:
            logger.warning(f"Password reset failed — user not found id:{user_id}")
            raise HTTPException(status_code=404, detail=f'user does not exist in db')

        if new_password != confirm_new_pw:
            logger.warning(f"Password reset failed — passwords do not match user:{user_id}")
            raise HTTPException(400, detail="Passwords do not match")

        if user:
            if new_password == confirm_new_pw:

                hashed_pw     = utils.hash(new_password)
                user.password = hashed_pw
                db.commit()
                db.refresh(user)
                #print("congratssss")
                logger.info(f"Password updated successfully — user:{user_id}")
                return {"msg": "password updated successfully"}
            else:
                logger.warning(f"Password reset failed — passwords not similar user:{user_id}")
                raise HTTPException(status_code=400, detail=f'passwords are not similar')

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password reset failed — error:{e}")
        raise HTTPException(status_code=500, detail="Password reset failed")