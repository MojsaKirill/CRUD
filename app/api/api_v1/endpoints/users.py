from typing import Any

from fastapi import APIRouter

from apps.auth import crud
from apps.auth.schema import UserView, UserCreate

router = APIRouter()


@router.post('/create', response_model=UserView, status_code=201)
async def create_user(item: UserCreate) -> Any:
    result = await crud.create(obj_in=item)
    return result
