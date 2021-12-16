from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from apps.auth import crud
from apps.auth.model import User
from apps.auth.schema import UserUpdate, UserView, UserCreate, UserViewMe
from core.security import get_current_user

router = APIRouter()


@router.get('/me', response_model=UserViewMe)
async def get_user_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


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
    result = await crud.create_user(obj_in=item)
    return result


@router.put('/{obj_id}', response_model=UserView)
async def update_user(obj_id: int, item: UserUpdate, user: User = Depends(get_current_user)) -> Any:
    obj_db = await crud.get(id=obj_id)
    if not obj_db:
        raise HTTPException(status_code=404, detail='User not found!')
    result = await crud.update_user(obj_db=obj_db, obj_in=item, user=user)
    return result
