from fastapi import FastAPI, APIRouter, File, UploadFile

            

router= APIRouter(prefix='/img_based_search',tags=['img_based_search'])

router.post('/')
def img_based_search():
    print("hiii")
    return 'hi'
  

   