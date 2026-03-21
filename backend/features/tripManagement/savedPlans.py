from fastapi import FastAPI, APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from backend.login import database, orm_model, oauth2
from backend.logger import logger

router = APIRouter(prefix='/savedPlans', tags=['savedPlans'])


@router.post('/')
def saved_plans(
    destination: str = Form(...),
    plan: str = Form(...),
    db: Session = Depends(database.get_db),
    current_user = Depends(oauth2.current_user_cookie)
):
    #print("save plan api loaded")
    logger.info(f"Save plan requested — user:{current_user.id} destination:{destination}")
    try:
        user_id = current_user.id
        #print(user_id)

        existing = db.query(orm_model.savedPlans)\
            .filter(
                orm_model.savedPlans.user_id == user_id,
                orm_model.savedPlans.plan == plan
            ).first()

        if existing:
            logger.warning(f"Plan already saved — user:{user_id} destination:{destination}")
            raise HTTPException(status_code=400, detail="plan already in saved plans")

        if user_id is None:
            logger.warning("User not found during save plan")
            raise HTTPException(status_code=404, detail=f'user not found')

        plan_obj = orm_model.savedPlans(user_id=user_id, destination=destination, plan=plan)
        #print("plan obj created")
        db.add(plan_obj)
        #print("plan added to db")
        db.commit()
        #print("ok final")
        logger.info(f"Plan saved successfully — user:{user_id} destination:{destination}")
        return {"message": f"plan is saved"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to save plan — user:{current_user.id} error:{e}")
        raise HTTPException(status_code=500, detail="Failed to save plan")


@router.get('/get')
def get_savedPlans(
    db: Session = Depends(database.get_db),
    current_user = Depends(oauth2.current_user_cookie)
):
    #print("get saved destinations api loaded")
    logger.info(f"Get saved plans requested — user:{current_user.id}")
    try:
        user_id = current_user.id
        plans = db.query(orm_model.savedPlans)\
            .filter(orm_model.savedPlans.user_id == user_id).all()
        #print(plans)
        logger.info(f"Saved plans fetched — user:{user_id} count:{len(plans)}")
        return {"response": plans}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch saved plans — user:{current_user.id} error:{e}")
        raise HTTPException(status_code=500, detail="Failed to load saved plans")


@router.delete('/delete/{plan_id}')
def deletePlan(
    plan_id: int,
    db: Session = Depends(database.get_db),
    current_user = Depends(oauth2.current_user_cookie)
):
    logger.info(f"Delete plan requested — user:{current_user.id} plan_id:{plan_id}")
    try:
        deleted_plan = db.query(orm_model.savedPlans)\
            .filter(
                orm_model.savedPlans.id == plan_id,
                orm_model.savedPlans.user_id == current_user.id
            ).first()

        if not deleted_plan:
            logger.warning(f"Plan not found — user:{current_user.id} plan_id:{plan_id}")
            raise HTTPException(status_code=404, detail="Plan not found")

        db.delete(deleted_plan)
        db.commit()
        logger.info(f"Plan deleted — user:{current_user.id} plan_id:{plan_id}")
        return {"response": "plan deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete plan — user:{current_user.id} plan_id:{plan_id} error:{e}")
        raise HTTPException(status_code=500, detail="Failed to delete plan")