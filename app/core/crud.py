from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DBOperationError, DuplicatedEntryError
from db.session import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        row = await db.execute(select(self.model).where(self.model.id == id))
        result = row.scalar_one_or_none()
        return result

    async def get_list(self, db: AsyncSession, *,
                       skip: int = 0, limit: int = 100) -> List[ModelType]:
        rows = await db.execute(select(self.model).offset(skip).limit(limit))
        results = rows.scalars().all()
        return results

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        obj_db = self.model(**obj_in_data)
        async with write_to_db(db) as written:
            db.add(obj_db)
            result = written
        if result:
            await db.refresh(obj_db)
            return obj_db

        # try:
        #     await db.commit()
        #     await db.refresh(obj_db)
        #     return obj_db
        # except SQLAlchemyError as ex:
        #     await db.rollback()
        #     raise HTTPException(status_code=422, detail=f'The record is already exist. Error: {ex}')

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
        except SQLAlchemyError as ex:
            await db.rollback()
            raise HTTPException(status_code=422, detail=f'Error delete record. Error: {ex}')


@asynccontextmanager
async def write_to_db(db: AsyncSession) -> AsyncIterator[bool]:
    try:
        yield True
        await db.commit()
    except SQLAlchemyError as ex:
        await db.rollback()
        raise DBOperationError(f'Error: {ex}')
