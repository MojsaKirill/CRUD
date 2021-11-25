from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.config import settings
from db.session import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        if settings.FUTURE:
            sql = select(self.model).where(self.model.id == id)
            result = db.execute(sql).scalar_one_or_none()
        else:
            result = db.query(self.model).filter(self.model.id == id).first()
        return result

    def get_list(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        if settings.FUTURE:
            sql = select(self.model).offset(skip).limit(limit)
            results = db.execute(sql).scalars().all()
        else:
            results = db.query(self.model).offset(skip).limit(limit).all()
        return results

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        obj_db = self.model(**obj_in_data)
        db.add(obj_db)
        db.commit()
        db.refresh(obj_db)
        return obj_db

    def update(self, db: Session, *, obj_db: ModelType,
               obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(obj_db)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(obj_db, field, update_data[field])
        db.add(obj_db)
        db.commit()
        db.refresh(obj_db)
        return obj_db

    def delete(self, db: Session, *, id: int) -> ModelType:
        obj_db = self.get(db, id)
        db.delete(obj_db)
        db.commit()
        return obj_db
