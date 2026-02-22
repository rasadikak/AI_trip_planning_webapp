from fastapi import APIRouter, Depends, HTTPException,Form

from sqlalchemy.orm import Session
from backend.login import database,orm_model,utils

router= APIRouter(prefix='/forget_pw')


@router.post('/request_reset')
def request_reset():
    pass
#process sending email using jwt
#forget_password.html -chnge password. email ekata ena link eken ynne mekata
#meka submit dunnma password update wela yata ed point ek run wenw





























@router.post('/')
def forget_password(email:str=Form(...), new_password:str=Form(...),confirm_new_pw:str=Form(...) ,db:Session= Depends(database.get_db)):
    #print(email)
    #print(new_password)
    #print(confirm_new_pw)
    
    
    user= db.query(orm_model.User).filter(orm_model.User.email==email).first()
    if not user:
        raise HTTPException(status_code=404, detail=f'user does not exist in db')
    if user:
         if new_password== confirm_new_pw:
             
         
             hashed_pw= utils.hash(new_password)
             
             user.password= hashed_pw
             
             
             db.commit()
             db.refresh(user)
             print("congratssss")
         else:    
         
            raise HTTPException(status_code=400, detail=f'passwords are not similar')