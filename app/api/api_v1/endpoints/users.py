from typing import Any, List

from fastapi import APIRouter, HTTPException

from apps.auth import crud
from apps.auth.schema import UserFromDB, UserView, UserCreate

router = APIRouter()


@router.get('/{obj_id}', response_model=UserView)
async def get_user(obj_id: int) -> Any:
    result = await crud.get(id=obj_id)
    if not result:
        raise HTTPException(status_code=404, detail='User not found!')
    return result


@router.get('/', response_model=List[UserView])
async def list_users(skip: int = 0, limit: int = 100) -> Any:
    results = await crud.get_list(skip=skip, limit=limit)
    return results


@router.post('/create', response_model=UserView, status_code=201)
async def create_user(item: UserCreate) -> Any:
    result = await crud.create(obj_in=item)
    return result
