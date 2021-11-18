from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from api import deps

router = APIRouter()


@router.get('/', response_model=List[schemas.User])
def list_users(db: Session = Depends(deps.get_db),
               skip: int = 0, limit: int = 100) -> Any:
    users = crud.user.get_list(db, skip=skip, limit=limit)
    return users


@router.post('/', response_model=schemas.User)
def create_user(*, db: Session = Depends(deps.get_db), user_in: schemas.UserCreate) -> Any:
    user = crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(status_code=400,
                            detail='The user with this username already exists.')
    if user_in.email:
        user = crud.user.get_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(status_code=400,
                                detail='The user with this email already exists.')
    user = crud.user.create(db, obj_in=user_in)
    return user
