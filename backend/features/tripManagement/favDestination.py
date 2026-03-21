from fastapi import FastAPI, APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from backend.login import database, orm_model, oauth2
from backend.logger import logger

router = APIRouter(prefix='/favDestination', tags=['favDestination'])


@router.post('/')
def add_fav_destination(
    destination: str = Form(...),
    db: Session = Depends(database.get_db),
    current_user = Depends(oauth2.current_user_cookie)
):
    #print("fav dest api loaded")
    logger.info(f"Add favourite requested — user:{current_user.id} destination:{destination}")
    try:
        user_id = current_user.id
        #print(user_id)

        existing = db.query(orm_model.favouritePlaces)\
            .filter(
                orm_model.favouritePlaces.user_id == user_id,
                orm_model.favouritePlaces.destination == destination
            ).first()

        if existing:
            logger.warning(f"Destination already in favourites — user:{user_id} destination:{destination}")
            raise HTTPException(status_code=400, detail="Destination already in favourites")

        if user_id is None:
            logger.warning("User not found during add favourite")
            raise HTTPException(status_code=404, detail=f'user not found')

        destination_obj = orm_model.favouritePlaces(user_id=user_id, destination=destination)
        #print('dest obj created')
        db.add(destination_obj)
        #print('dest obj added to db')
        db.commit()
        #print('ok 2')
        logger.info(f"Favourite added — user:{user_id} destination:{destination}")
        return {"message": f"{destination} added to favourites"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add favourite — user:{current_user.id} error:{e}")
        raise HTTPException(status_code=500, detail="Failed to save favourite")


@router.get('/get')
def get_favDestinations(
    db: Session = Depends(database.get_db),
    current_user = Depends(oauth2.current_user_cookie)
):
    #print("get fav destination api loaded")
    logger.info(f"Get favourites requested — user:{current_user.id}")
    try:
        user_id = current_user.id
        destinations = db.query(orm_model.favouritePlaces)\
            .filter(orm_model.favouritePlaces.user_id == user_id).all()
        #print(destinations)
        logger.info(f"Favourites fetched — user:{user_id} count:{len(destinations)}")
        if destinations:
            return {"response": destinations}
        return {"response": []}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch favourites — user:{current_user.id} error:{e}")
        raise HTTPException(status_code=500, detail="Failed to load favourites")


@router.delete('/delete/{fav_id}')
def delete_fav_destination(
    fav_id: int,
    db: Session = Depends(database.get_db),
    current_user = Depends(oauth2.current_user_cookie)
):
    logger.info(f"Delete favourite requested — user:{current_user.id} fav_id:{fav_id}")
    try:
        fav = db.query(orm_model.favouritePlaces)\
            .filter(
                orm_model.favouritePlaces.id == fav_id,
                orm_model.favouritePlaces.user_id == current_user.id
            ).first()

        if not fav:
            logger.warning(f"Favourite not found — user:{current_user.id} fav_id:{fav_id}")
            raise HTTPException(status_code=404, detail="Not found")

        db.delete(fav)
        db.commit()
        logger.info(f"Favourite deleted — user:{current_user.id} fav_id:{fav_id}")
        return {"message": "Deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete favourite — user:{current_user.id} fav_id:{fav_id} error:{e}")
        raise HTTPException(status_code=500, detail="Failed to delete favourite")