from fastapi import FastAPI,APIRouter, Depends, HTTPException, status_code
from sqlalchemy.orm import Session
from backend.login import database,orm_model, oauth2

router= APIRouter(prefix=['favDestination'], tags=['favDestination'])

@router.post('/')
def add_fav_destination(destination:str, 
                        db:Session=Depends(database.get_db), 
                        current_user=Depends(oauth2.current_user_cookie)):
    
    user_id= current_user.id

    existing = db.query(orm_model.favouritePlaces)\
        .filter(
            orm_model.favouritePlaces.user_id == user_id,
            orm_model.favouritePlaces.destination == destination
        ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Destination already in favourites")
    
    if user_id is None:
        raise HTTPException(status_code= 404, detail=f'user not found')
    destination_obj= orm_model.favouritePlaces(user_id=user_id,  destination=destination)
    db.add(destination_obj)
    db.commit()
    return {"message": f"{destination} added to favourites"}
    