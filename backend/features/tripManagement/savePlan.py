from fastapi import FastAPI,APIRouter, Depends, HTTPException,Form
from sqlalchemy.orm import Session
from backend.login import database,orm_model, oauth2

router= APIRouter(prefix='/savedPlans', tags=['savedPlans'])

@router.post('/')
def saved_plans(destination:str=Form(...), 
                plan:str=Form(...),
                db:Session=Depends(database.get_db), 
                current_user=Depends(oauth2.current_user_cookie)):
    
    user_id= current_user.id

    existing = db.query(orm_model.savedPlans)\
        .filter(
            orm_model.savedPlans.user_id == user_id,
            orm_model.savedPlans.plan == plan
        ).first()

    if existing:
        raise HTTPException(status_code=400, detail="plan already in saved plans")
    
    if user_id is None:
        raise HTTPException(status_code= 404, detail=f'user not found')
    plan_obj= orm_model.savedPlans(user_id=user_id,  destination=destination, plan=plan)
    db.add(plan_obj)
    db.commit()
    return {"message": f"plan is saved"}
    