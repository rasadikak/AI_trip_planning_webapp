from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from backend.login import database,orm_model
from backend.login.routers.email_verify_for_signup import send_mail


router= APIRouter(prefix='/verify_email_for_login')

@router.post("/")
async def email_verify_for_login(email: str=Form(...), db: Session = Depends(database.get_db)):
    user = db.query(orm_model.User).filter(orm_model.User.email == email).first()
    if not user:
        raise HTTPException(404, "User not found")
    if user.is_verified:
        return {"msg": "User already verified"}
    await send_mail(email, db)  
    return {"msg": "Verification email sent again"}