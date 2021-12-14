from typing import List, Optional

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from apps.auth.model import User
from apps.auth.schema import UserCreate
from db.session import SessionManager

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
db = SessionManager()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get(id: int) -> Optional[User]:
    async with db.obtain_session() as sess:
        select_stmt = select(User).where(User.id == id)
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def get_user_auth(user_name: str, user_pass: str) -> Optional[User]:
    select_stmt = select(User.password)
    select_stmt = select_stmt.where(User.username == user_name)
    select_stmt = select_stmt.where(User.password == get_password_hash(user_pass))
    async with db.obtain_session() as sess:
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def get_list(skip: int = 0, limit: int = 100) -> List[User]:
    async with db.obtain_session() as sess:
        select_stmt = select(User).offset(skip).limit(limit)
        results = (await sess.execute(select_stmt)).scalars().all()
    return results


async def create(obj_in: UserCreate) -> Optional[User]:
    insert_data = obj_in.dict(exclude_unset=True)
    insert_data['password'] = get_password_hash(insert_data['password'])
    async with db.obtain_session() as sess:
        insert_stmt = insert(User).values(**insert_data).returning(User)
        result = (await sess.execute(insert_stmt)).mappings().first()
    return result
