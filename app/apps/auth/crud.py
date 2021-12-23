from typing import Any, Dict, List, Optional, Union

from sqlalchemy import select, insert, update, func

from apps.auth.model import User
from apps.auth.schema import UserCreate, UserRegister, UserUpdate
from core.exceptions import credentials_exception, user_already_exist, email_already_exist
from core.utils import obj_to_dict, get_password_hash
from db.session import SessionManager

db = SessionManager()


async def get(id: int) -> Optional[User]:
    select_stmt = select(User).where(User.id == id)
    async with db.obtain_session() as sess:
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def get_user_by_name(user_name: str) -> Optional[User]:
    select_stmt = select(User).where(func.upper(User.username) == func.upper(user_name))
    async with db.obtain_session() as sess:
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def get_user_by_email(user_email: str) -> Optional[User]:
    select_stmt = select(User).where(func.upper(User.email) == func.upper(user_email))
    async with db.obtain_session() as sess:
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def check_username_or_email(user_name: str, user_email: str = None):
    select_stmt = select(User.id).where(func.upper(User.username) == func.upper(user_name))
    #TODO
    async with db.obtain_session() as sess:
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    if result:
        raise user_already_exist
    if user_email:
        select_stmt = select(User.id).where(func.upper(User.email) == func.upper(user_email))
        async with db.obtain_session() as sess:
            result = (await sess.execute(select_stmt)).scalar_one_or_none()
        if result:
            raise email_already_exist
    #TODO
    return None


async def get_list(skip: int = 0, limit: int = 100) -> List[User]:
    select_stmt = select(User).offset(skip).limit(limit)
    async with db.obtain_session() as sess:
        results = (await sess.execute(select_stmt)).scalars().all()
    return results


#TOOD
async def create_user(obj_in: Union[UserCreate, UserRegister, Dict[str, Any]]) -> Optional[User]:
    insert_data = obj_to_dict(obj_in)
    insert_data['password'] = get_password_hash(insert_data['password'])
    obj_in.password = get_password_hash(obj_in.password)
    insert_stmt = insert(User).values(User(username=obj_in.username, )).returning(User)
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
