from typing import Optional

from sqlalchemy.orm import Session

from core.security import get_password_hash
from crud.base import CRUDBase
from models import User
from schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(username=obj_in.username,
                      email=obj_in.email,
                      hashed_password=get_password_hash(obj_in.password),
                      is_superuser=obj_in.is_superuser, )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # def is_active(self, user: User) -> bool:
    #     return user.is_active

    # def is_superuser(self, user: User) -> bool:
    #     return user.is_superuser


user = CRUDUser(User)
