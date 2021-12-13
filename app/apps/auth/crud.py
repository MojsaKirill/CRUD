from typing import Optional

from apps.auth.model import User
from apps.auth.schema import UserCreate
from core.security import get_password_hash
from db.session import SessionManager

db = SessionManager()


async def create(obj_in: UserCreate) -> Optional[User]:
    insert_data = obj_in.dict(exclude_unset=True)
    insert_data['password'] = get_password_hash(insert_data['password'])
    obj_db = User(**insert_data)
    async with db.obtain_session() as sess:
        sess.add(obj_db)
    return obj_db
