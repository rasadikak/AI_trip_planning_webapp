from fastapi import APIRouter, HTTPException, Form, Depends

from backend.login import database, orm_model, oauth2
from sqlalchemy.orm import Session
from backend.logger import logger

import re

router= APIRouter(prefix='/profile', tags=['profile'])

@router.put('/editName')
def editName(new_name:str=Form(...),
             db:Session=Depends(database.get_db),
             current_user=Depends(oauth2.current_user_cookie)):
    
    try:
        user_id= current_user.id

        if not re.fullmatch(r"[A-Za-z ]{3,}", name.strip()):
            logger.warning(f"Name update failed — invalid name: {new_name}")
            raise HTTPException(
                status_code=400,
                detail="Name must be at least 3 characters and contain only letters and spaces"
            )
        
        if new_name.strip() == current_user.name:
            raise HTTPException(status_code=400, detail="New name is same as current name")
        

        user= db.query(orm_model.User).filter(orm_model.User.id==user_id).first()
        if not user:
            logger.warning(f" user {user_id} does not exist")
            raise HTTPException(status_code=404, detail="User not found")

        user.name= new_name
        
        db.commit()
        db.refresh(user)
        logger.info(f"user {user_id} updated his name ")
        raise HTTPException(status_code=200, detail=f"name updated successfully")

    except HTTPException:
        raise 

    except Exception as e:
        logger.error(f"Name update failed — user:{current_user.id} error:{e}")
        raise HTTPException(status_code=500, detail="Failed to update name")



    
    