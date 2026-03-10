from fastapi import APIRouter

router= APIRouter(prefix='/trip_planner', tags=['trip_planner'])

@router.post('/')
def trip_planner():
    pass