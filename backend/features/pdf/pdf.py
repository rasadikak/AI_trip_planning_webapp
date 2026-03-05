from fastapi import APIRouter, FastAPI, HTTPException

router= APIRouter(prefix='/pdf', tags=['pdf'])


@router.get('/')
def pdf():
    print('jjj')
    return 'ghj'