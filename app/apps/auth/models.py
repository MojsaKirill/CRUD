from sqlalchemy import Column, Integer, String
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from db.session import Base, database
from schemas.user import UserDB


class UserTable(Base, SQLAlchemyBaseUserTable):
    id = Column(Integer, primary_key=True)
    username = Column(String(length=50), unique=True, index=True, nullable=False)
    email = Column(String(length=320), unique=True, index=True)


users = UserTable.__table__


async def get_user_db():
    yield SQLAlchemyUserDatabase(UserDB, database, users)
