from fastapi import APIRouter,Form

router= APIRouter(prefix='/trip_planner', tags=['trip_planner'])

@router.post('/')
def trip_planner(destinationType:str= Form(...), budget:str=Form(...), numDays:int=Form(...) ,numPeople:int=Form(...),accommodation:str=Form(...), foodPreference:str=Form(...)):
    pass