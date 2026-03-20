from fastapi import FastAPI,APIRouter, Depends, HTTPException,Form
from sqlalchemy.orm import Session
from backend.login import database,orm_model, oauth2

router= APIRouter(prefix='/savedPlans', tags=['savedPlans'])

@router.post('/')
def saved_plans(destination:str=Form(...), 
                plan:str=Form(...),
                db:Session=Depends(database.get_db), 
                current_user=Depends(oauth2.current_user_cookie)):
    #print("save plan api loaded")
    
    user_id= current_user.id
    #print(user_id)

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
    #print("plan obj created")
    db.add(plan_obj)
    #print("plan added to db")
    db.commit()
    #print("ok final")
    return {"message": f"plan is saved"}
    




@router.get('/get')
def get_savedPlans(db:Session=Depends(database.get_db),
                        current_user= Depends(oauth2.current_user_cookie)):
    #print("get saved destinations api loaded")
    user_id= current_user.id
    plans= db.query(orm_model.savedPlans).filter(orm_model.savedPlans.user_id==user_id).all()
    #print(plans)
    return {"response":plans}





@router.delete('/delete/{plan_id}')
def deletePlan(plan_id:int ,db:Session=Depends(database.get_db),
                current_user= Depends(oauth2.current_user_cookie)
               
                ):
    
    deleted_plan= db.query(orm_model.savedPlans).filter(orm_model.savedPlans.id==plan_id, orm_model.savedPlans.user_id == current_user.id).first()
    if not deleted_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.delete(deleted_plan)
    db.commit()
    return {"response":"plan deleted successfully"}
