from fastapi import APIRouter

from core.config import settings

router = APIRouter(tags=['Home'])


@router.get('/')
async def home():
    return {'Welcome to API': settings.PROJECT_NAME}
