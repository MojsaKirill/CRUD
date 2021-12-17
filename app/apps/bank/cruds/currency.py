from typing import Any, Optional, List, Union, Dict

from fastapi import HTTPException
from sqlalchemy import and_, desc, func, select, delete, insert, update
from starlette import status
from starlette.responses import JSONResponse

from apps.bank.models.currency import Currency
from apps.bank.schemas.currency import CurrencyCreate, CurrencyRateOnDate, CurrencyUpdate
from core.utils import obj_to_dict
from db.session import SessionManager

db = SessionManager()


async def get(id: Any) -> Optional[Currency]:
    select_stmt = select(Currency).where(Currency.id == id)
    async with db.obtain_session() as sess:
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def get_code_rate_on_date(item: CurrencyRateOnDate) -> Optional[Currency]:
    select_stmt = select(Currency).where(
        and_(func.upper(Currency.code) == func.upper(item.code),
             Currency.date_start <= item.date_start)
    ).order_by(desc(Currency.date_start)).limit(1)
    async with db.obtain_session() as sess:
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def get_list(skip: int = 0, limit: int = 100) -> List[Currency]:
    select_stmt = select(Currency).offset(skip).limit(limit)
    async with db.obtain_session() as sess:
        results = (await sess.execute(select_stmt)).scalars().all()
    return results


async def create_currency(obj_in: Union[CurrencyCreate, Dict[str, Any]]) -> Optional[Currency]:
    insert_data = obj_to_dict(obj_in)
    insert_stmt = insert(Currency).values(**insert_data).returning(Currency)
    async with db.obtain_session() as sess:
        result = (await sess.execute(insert_stmt)).mappings().first()
    return result


async def update_currency(obj_db: Currency,
                          obj_in: Union[CurrencyUpdate, Dict[str, Any]]) -> Currency:
    update_data = obj_to_dict(obj_in)
    update_stmt = update(Currency).where(Currency.id == obj_db.id)
    update_stmt = update_stmt.values(**update_data).returning(Currency)
    async with db.obtain_session() as sess:
        result = (await sess.execute(update_stmt)).mappings().first()
    return result


async def remove_currency(id: int) -> Any:
    delete_stmt = delete(Currency).where(Currency.id == id)
    async with db.obtain_session() as sess:
        result = await sess.execute(delete_stmt)
    if result.rowcount == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f'Record with id={id} not found')
