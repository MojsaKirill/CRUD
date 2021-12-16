from typing import Any, Dict, List, Optional, Union

from sqlalchemy import select, insert, update

from apps.auth.model import User
from apps.auth.schema import UserCreate, UserUpdate
from core.exceptions import credentials_exception
from core.utils import obj_to_dict, get_password_hash
from db.session import SessionManager

db = SessionManager()


async def get(id: int) -> Optional[User]:
    select_stmt = select(User).where(User.id == id)
    async with db.obtain_session() as sess:
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def get_user_auth(user_name: str) -> Optional[User]:
    select_stmt = select(User).where(User.username == user_name)
    async with db.obtain_session() as sess:
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def get_list(skip: int = 0, limit: int = 100) -> List[User]:
    select_stmt = select(User).offset(skip).limit(limit)
    async with db.obtain_session() as sess:
        results = (await sess.execute(select_stmt)).scalars().all()
    return results


async def create_user(obj_in: Union[UserCreate, Dict[str, Any]]) -> Optional[User]:
    insert_data = obj_to_dict(obj_in)
    insert_data['password'] = get_password_hash(insert_data['password'])
    insert_stmt = insert(User).values(**insert_data).returning(User)
    async with db.obtain_session() as sess:
        result = (await sess.execute(insert_stmt)).mappings().first()
    return result


async def update_user(obj_db: User, obj_in: Union[UserUpdate, Dict[str, Any]], user: User) -> User:
    if not user.banker and obj_db.id != user.id:
        raise credentials_exception
    update_data = obj_to_dict(obj_in)
    update_stmt = update(User).where(User.id == obj_db.id).values(**update_data).returning(User)
    async with db.obtain_session() as sess:
        result = (await sess.execute(update_stmt)).mappings().first()
    return result
