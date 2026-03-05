from fastapi import APIRouter

router= APIRouter(prefix='/searchImage', tags=['searchImage'])

router.get('/')
def image_search():
    print('immm')
    return 'hhhss'