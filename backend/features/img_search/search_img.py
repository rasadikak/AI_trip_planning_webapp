from fastapi import APIRouter

router= APIRouter(prefix='/image_search', tags=['image_search'])

router.get('/')
def image_search():
    print('immm')
    return 'hhhss'