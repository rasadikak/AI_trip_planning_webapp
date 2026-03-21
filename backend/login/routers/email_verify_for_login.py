from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from backend.login import database, orm_model
from backend.login.routers.email_verify_for_signup import send_mail
from backend.logger import logger

router = APIRouter(prefix='/verify_email_for_login')


@router.post("/")
async def email_verify_for_login(
    email: str = Form(...),
    db: Session = Depends(database.get_db)
):
    logger.info(f"Email verification for login requested — email:{email}")
    try:
        user = db.query(orm_model.User).filter(orm_model.User.email == email).first()

        if not user:
            logger.warning(f"Verification failed — user not found: {email}")
            raise HTTPException(404, "User not found")

        if user.is_verified:
            logger.info(f"User already verified — email:{email}")
            return {"msg": "User already verified"}

        await send_mail(email, db)
        logger.info(f"Verification email sent — email:{email}")
        return {"msg": "Verification email sent again"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Email verification failed — email:{email} error:{e}")
        raise HTTPException(status_code=500, detail="Failed to send verification email")