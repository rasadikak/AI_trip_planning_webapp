from fastapi import FastAPI,APIRouter, Depends, HTTPException,Form
from sqlalchemy.orm import Session
from backend.login import database,orm_model, oauth2

router= APIRouter(prefix='/favDestination', tags=['favDestination'])

@router.post('/')
def add_fav_destination(destination:str=Form(...), 
                        db:Session=Depends(database.get_db), 
                        current_user=Depends(oauth2.current_user_cookie)):
    print("fav dest api loaded")
    
    user_id= current_user.id
    print(user_id)

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
    print('dest obj created')
    db.add(destination_obj)
    print('dest obj added to db')
    db.commit()
    print('ok 2')
    return {"message": f"{destination} added to favourites"}





@router.get('/get')
def get_favDestinations(db:Session=Depends(database.get_db),
                        current_user= Depends(oauth2.current_user_cookie)):
    print("get fav destination api loaded")
    user_id= current_user.id
    destinations= db.query(orm_model.favouritePlaces).filter(orm_model.favouritePlaces.user_id==user_id)
    print(destinations)
    if destinations:
        return {"response":destinations}




@router.delete('/delete/{id}')
def del_favDestinations(db:Session=Depends(database.get_db),
                        dest_id:id=Form(...)):
    print("delete fav destination api loaded")


    

    destination= db.query(orm_model.favouritePlaces).filter(orm_model.favouritePlaces.id==dest_id)
    print(destination)
    if not destination:
        return HTTPException(status_code=404, detail=f'destination not found in db')
    db.delete(destination)
    db.commit()
    return {"msg":"favourite destination deleted succeesfully"}
