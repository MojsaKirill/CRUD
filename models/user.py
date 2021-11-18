from sqlalchemy import Column
from sqlalchemy.sql import sqltypes as _type
from db.base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(_type.Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(_type.String, unique=True, index=True, nullable=False)
    email = Column(_type.String, unique=True, index=True)
    hashed_password = Column(_type.String, nullable=False)
    is_active = Column(_type.Boolean(), default=True)
    is_superuser = Column(_type.Boolean(), default=False)

    # def __repr__(self):
    #     return f'User({self.id!r}, {self.username!r}, {self.email!r}, {self.is_superuser!r}, {self.is_active!r})'
