from fastapi import FastAPI, APIRouter, File, UploadFile


router= APIRouter(prefix='/img_based_search')

router.post('/')
async def img_based_search(img: UploadFile = File(...)):
      
    content = await img.read()  
    print(f"Received file: {img.filename}, size: {len(content)} bytes")
    return {"filename": img.filename, "size": len(content)}
    
