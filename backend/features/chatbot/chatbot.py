from fastapi import APIRouter

router= APIRouter(prefix="/chatbot", tags=['chatbot'])

@router.post('/')
def chatbot(text:str):
    pass