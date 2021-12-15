from typing import Any, Dict, List, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, insert

from apps.auth.model import User
from apps.auth.schema import UserCreate, UserUpdate
from core.utils import get_password_hash
from db.session import SessionManager

db = SessionManager()


async def get(id: int) -> Optional[User]:
    async with db.obtain_session() as sess:
        select_stmt = select(User).where(User.id == id)
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def get_user_auth(user_name: str) -> Optional[User]:
    async with db.obtain_session() as sess:
        select_stmt = select(User).where(User.username == user_name)
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def get_list(skip: int = 0, limit: int = 100) -> List[User]:
    async with db.obtain_session() as sess:
        select_stmt = select(User).offset(skip).limit(limit)
        results = (await sess.execute(select_stmt)).scalars().all()
    return results


async def create(obj_in: Union[UserCreate, Dict[str, Any]]) -> Optional[User]:
    if isinstance(obj_in, dict):
        insert_data = obj_in
    else:
        insert_data = obj_in.dict(exclude_unset=True)
    insert_data['password'] = get_password_hash(insert_data['password'])
    async with db.obtain_session() as sess:
        insert_stmt = insert(User).values(**insert_data).returning(User)
        result = (await sess.execute(insert_stmt)).mappings().first()
    return result


async def update(obj_db: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    obj_data = jsonable_encoder(obj_db)

    for field in obj_data:
        if field in update_data:
            setattr(obj_db, field, update_data[field])

    async with db.obtain_session() as sess:
        sess.add(obj_db)
    return obj_db
