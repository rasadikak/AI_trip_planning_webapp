from fastapi import FastAPI, APIRouter, status, Form, HTTPException, Depends
import re
from backend.login import database, orm_model, schemas
from sqlalchemy.orm import Session
from backend.login import utils
from typing import List
from fastapi.responses import JSONResponse, RedirectResponse
from backend.login.routers import email_verify_for_signup
from backend.logger import logger

router = APIRouter(prefix='/register', tags=['register'])


@router.get('/test')
def msg():
    #print("fff")
    return 'bye'


def validate_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    if password != confirm_password:
        logger.warning(f"Registration validation failed — passwords do not match email:{email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='passwords_not_match')

    if not re.fullmatch(r"[A-Za-z ]{3,}", name):
        logger.warning(f"Registration validation failed — invalid name: {name}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid_name"
        )

    if not re.fullmatch(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        logger.warning(f"Registration validation failed — invalid email: {email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid_email")

    existing_email = db.query(orm_model.User).filter(orm_model.User.email == email).first()
    if existing_email:
        logger.warning(f"Registration validation failed — email already exists: {email}")
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='email_exists')

    if not re.fullmatch(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$", password):
        logger.warning(f"Registration validation failed — weak password email:{email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="weak_password"
        )

    if len(password) > 64:
        logger.warning(f"Registration validation failed — password too long email:{email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password_too_long")

    return {"name": name, "email": email, "password": password}


@router.post('/', status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
async def create_user(
    db: Session = Depends(database.get_db),
    user = Depends(validate_user)
):
    #print("before")
    logger.info(f"User registration attempt — email:{user['email']}")
    try:
        hashed_pw = utils.hash(user['password'])
        #print("pw hashed suucessfully")
        new_user = orm_model.User(name=user['name'], email=user['email'], password=hashed_pw)
        #print("new user cretaed successfully")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        if new_user.is_verified == False:
            await email_verify_for_signup.send_mail(new_user.email, db)
            print("sent mail successufully")

        #print("after")
        logger.info(f"User registered successfully — email:{user['email']} id:{new_user.id}")
        return RedirectResponse(url='/frontend/home/check_your_mail.html', status_code=302)

    except HTTPException as e:
        # Redirect back to register page with error code from validate_user
        logger.warning(f"Registration validation error — {e.detail}")
        return RedirectResponse(
            url=f'/frontend/home/register.html?error={e.detail}',
            status_code=302
        )
    except Exception as e:
        logger.error(f"User registration failed — email:{user['email']} error:{e}")
        return RedirectResponse(
            url='/frontend/home/register.html?error=registration_failed',
            status_code=302
        )


#  email verification
@router.get('/admin', response_model=List[schemas.UserResponse])
def get_all(db: Session = Depends(database.get_db)):
    logger.info("Admin — get all users requested")
    try:
        users = db.query(orm_model.User).all()
        logger.info(f"Admin — returned {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Admin get all users failed — error:{e}")
        raise HTTPException(status_code=500, detail="Failed to fetch users")


@router.get('/admin/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(database.get_db)):
    logger.info(f"Admin — get user requested id:{id}")
    try:
        user = db.query(orm_model.User).filter(orm_model.User.id == id).first()
        if not user:
            logger.warning(f"Admin — user not found id:{id}")
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'user {id} does not exist')
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin get user failed — id:{id} error:{e}")
        raise HTTPException(status_code=500, detail="Failed to fetch user")


@router.delete('/delete/{id}')
def delete_user(id: int, db: Session = Depends(database.get_db)):
    logger.info(f"Admin — delete user requested id:{id}")
    try:
        user = db.query(orm_model.User).filter(orm_model.User.id == id).first()
        if not user:
            logger.warning(f"Admin — delete failed user not found id:{id}")
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'user {id} does not exist')
        db.delete(user)
        db.commit()
        logger.info(f"Admin — user deleted id:{id}")
        return JSONResponse(status.HTTP_204_NO_CONTENT, detail=f'user {id}  deleted')
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin delete user failed — id:{id} error:{e}")
        return RedirectResponse(
            url='/frontend/home/register.html?error=registration_failed',
            status_code=302
        )
