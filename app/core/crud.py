from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.exceptions import DuplicatedEntryError
from db.session import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        if settings.FUTURE:
            row = await db.execute(select(self.model).where(self.model.id == id))
            result = row.scalar_one_or_none()
        else:
            result = await db.query(self.model).filter(self.model.id == id).first()
        return result

    async def get_list(self, db: AsyncSession, *,
                       skip: int = 0, limit: int = 100) -> List[ModelType]:
        if settings.FUTURE:
            rows = await db.execute(select(self.model).offset(skip).limit(limit))
            results = rows.scalars().all()
        else:
            results = await db.query(self.model).offset(skip).limit(limit).all()
        return results

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        obj_db = self.model(**obj_in_data)
        db.add(obj_db)
        try:
            await db.commit()
            await db.refresh(obj_db)
            return obj_db
        except IntegrityError as ex:
            await db.rollback()
            raise DuplicatedEntryError(f'The record is already exist. Error: {ex.detail}')

    async def update(self, db: AsyncSession, *, obj_db: ModelType,
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
        try:
            await db.commit()
            await db.refresh(obj_db)
            return obj_db
        except IntegrityError as ex:
            await db.rollback()
            raise DuplicatedEntryError(f'The record is already exist. Error: {ex.detail}')

    async def delete(self, db: AsyncSession, *, id: int) -> ModelType:
        obj_db = await self.get(db, id)
        try:
            await db.delete(obj_db)
            await db.commit()
            return obj_db
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=422, detail='Error delete record.')
