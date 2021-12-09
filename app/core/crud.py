from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from starlette import status
from starlette.responses import JSONResponse

from db.session import Base, SessionManager

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.db = SessionManager()

    async def get(self, id: Any) -> Optional[ModelType]:
        async with self.db.obtain_session() as sess:
            row = await sess.execute(select(self.model).where(self.model.id == id))
        result = row.scalar_one_or_none()
        return result

    async def get_list(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        async with self.db.obtain_session() as sess:
            rows = await sess.execute(select(self.model).offset(skip).limit(limit))
        results = rows.scalars().all()
        return results

    async def create(self, *, obj_in: CreateSchemaType) -> Optional[ModelType]:
        insert_data = obj_in.dict(exclude_unset=True)
        obj_db = self.model(**insert_data)
        async with self.db.obtain_session() as sess:
            sess.add(obj_db)
        return obj_db

    async def update(self, *, obj_db: ModelType,
                     obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = jsonable_encoder(obj_db)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(obj_db, field, update_data[field])

        async with self.db.obtain_session() as sess:
            sess.add(obj_db)
        return obj_db

    async def delete(self, *, id: int) -> Any:
        async with self.db.obtain_session() as sess:
            result = await sess.execute(delete(self.model).where(self.model.id == id))
        if result.rowcount == 1:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(status_code=404, detail=f'Record with id={id} not found')
