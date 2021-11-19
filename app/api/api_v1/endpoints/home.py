from fastapi import APIRouter

from core.config import settings

router = APIRouter()


@router.get('/')
def home():
    return {'Welcome to API': settings.PROJECT_NAME}
