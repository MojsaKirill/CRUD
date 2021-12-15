from typing import Any, Optional, List, Union, Dict

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, insert
from starlette import status
from starlette.responses import JSONResponse

from apps.bank.models.currency import Currency
from apps.bank.schemas.currency import CurrencyCreate, CurrencyUpdate
from db.session import SessionManager

db = SessionManager()


async def get(id: Any) -> Optional[Currency]:
    async with db.obtain_session() as sess:
        row = await sess.execute(select(Currency).where(Currency.id == id))
    result = row.scalar_one_or_none()
    return result


async def get_list(skip: int = 0, limit: int = 100) -> List[Currency]:
    async with db.obtain_session() as sess:
        select_stmt = select(Currency).offset(skip).limit(limit)
        results = (await sess.execute(select_stmt)).scalars().all()
    return results


async def create(obj_in: Union[CurrencyCreate, Dict[str, Any]]) -> Optional[Currency]:
    if isinstance(obj_in, dict):
        insert_data = obj_in
    else:
        insert_data = obj_in.dict(exclude_unset=True)
    async with db.obtain_session() as sess:
        insert_stmt = insert(Currency).values(**insert_data).returning(Currency)
        result = (await sess.execute(insert_stmt)).mappings().first()
    return result


async def update(obj_db: Currency, obj_in: Union[CurrencyUpdate, Dict[str, Any]]) -> Currency:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    obj_data = jsonable_encoder(obj_db)

    for field in obj_data:
        if field in update_data:
            setattr(obj_db, field, update_data[field])

    async with db.obtain_session() as sess:
        sess.add(obj_db)
    return obj_db


async def remove(id: int) -> Any:
    async with db.obtain_session() as sess:
        result = await sess.execute(delete(Currency).where(Currency.id == id))
    if result.rowcount == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f'Record with id={id} not found')
