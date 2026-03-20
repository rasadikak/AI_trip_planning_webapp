from fastapi import APIRouter, Response, HTTPException, status
from fastapi.responses import RedirectResponse



router= APIRouter(prefix='/signout')

@router.api_route('/', methods=['GET','POST'])
def signout(response:Response):
    #print("one")
    response.delete_cookie(key='access_token')
    #print("seco")
    return RedirectResponse(url='/frontend/home/home.html', status_code=status.HTTP_302_FOUND)
    

#302= temporary redirect.
# fastapi doesnt allow adding a folder like frontend directly. so we should mount it first
# in main.py app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
#//frontend → the URL prefix people will visit in the browser.
#directory="frontend" → the local folder where your files are.
#name → an internal FastAPI name for reference.


