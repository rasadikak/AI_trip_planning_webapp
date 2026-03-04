from fastapi import APIRouter, FastAPI


router= APIRouter(prefix='/map', tags=['map'])

@router.get('/')
def map():
    print('map')
    return 'map'