from fastapi import FastAPI, APIRouter, Form, Depends, HTTPException
#from backend.main import app
from backend.login import orm_model, database, utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.login import oauth2
from fastapi.responses import RedirectResponse
from backend.logger import logger

router = APIRouter(prefix='/login', tags=['login'])


@router.post('/')
def login(
    user_credintials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    #print("before ok")
    logger.info(f"Login attempt — email:{user_credintials.username}")
    try:
        user = db.query(orm_model.User).filter(orm_model.User.email == user_credintials.username).first()

        if not user:
            logger.warning(f"Login failed — email not found: {user_credintials.username}")
            return RedirectResponse(
                    url='/frontend/home/login.html?error=email_not_found',
                    status_code=302
             )

        verify_pw = utils.verify(user_credintials.password, user.password)
        if verify_pw == False:
            #print("password wrong")
            logger.warning(f"Login failed — wrong password: {user_credintials.username}")
            return RedirectResponse(
                url='/frontend/home/login.html?error=wrong_password',
                status_code=302
            )

        if not user.is_verified:
            logger.warning(f"Login failed — email not verified: {user_credintials.username}")
            return RedirectResponse(
                url='/frontend/home/login.html?error=not_verified',
                status_code=302
            )

        access_token = oauth2.create_token({"user_id": user.id})

        response = RedirectResponse(url=f'/frontend/features/trip_planner.html', status_code=302)
        response.set_cookie(key="access_token", value=f"bearer {access_token}", httponly=True)
        #return {"access_token": access_token, "token_type":"bearer"}
        response.set_cookie(key="user_name", value=user.name)
        response.set_cookie(key="user_email", value=user.email)

        logger.info(f"Login successful — user:{user.id}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login crashed — email:{user_credintials.username} error:{e}")
        raise HTTPException(status_code=500, detail="Login failed. Please try again.")