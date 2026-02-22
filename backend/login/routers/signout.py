from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.login import database, oauth2


router= APIRouter(prefix='/signout')

@router.post('/')
def signout(db: Session= Depends(database.get_db), curruent_user:Session=Depends(oauth2.current_user)):
    pass
