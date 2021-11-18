from sqlalchemy.orm import Session

import crud
import schemas
from core.config import settings
from db.base import Base
from db.session import engine


def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine,
                             tables=Base.metadata.tables.values())

    user = crud.user.get_by_username(db, username=settings.FIRST_SUPERUSER_NAME)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_SUPERUSER_NAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,)
        user = crud.user.create(db, obj_in=user_in)
