from typing import Optional

from fastapi import APIRouter, Depends

from apps.auth.model import User
from core.config import settings
from core.security import get_current_user

router = APIRouter()


@router.get('/')
async def home(user: User = Depends(get_current_user)):
    return {f'{user.username} welcome to API': settings.PROJECT_NAME}
