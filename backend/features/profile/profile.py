from fastapi import APIRouter

router= APIRouter(prefix='/profile', tags=['profile'])

router.get('/')
def profile():
    print('prof')
    return 'prof'