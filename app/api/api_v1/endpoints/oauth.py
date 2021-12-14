from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse, Response

from core.security import auth_security

router = APIRouter()


@router.get('/login')
async def auth_login(auth: str = Depends(auth_security)):
    if not auth:
        response = Response(headers={}, status_code=401)
        return response

    try:
        print(auth)
        response = RedirectResponse(url='/docs')
        return response
    except:
        response = Response(headers={}, status_code=401)
        return response
