from typing import Any, List, Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete
from starlette import status
from starlette.responses import JSONResponse

from apps.bank.models.invoice import Invoice
from apps.bank.schemas.invoice import InvoiceCreate, InvoiceUpdate
from db.session import SessionManager

db = SessionManager()


async def get(id: Any) -> Optional[Invoice]:
    async with db.obtain_session() as sess:
        row = await sess.execute(select(Invoice).where(Invoice.id == id))
    result = row.scalar_one_or_none()
    return result


async def get_list(skip: int = 0, limit: int = 100) -> List[Invoice]:
    async with db.obtain_session() as sess:
        rows = await sess.execute(select(Invoice).offset(skip).limit(limit))
    results = rows.scalars().all()
    return results


async def create(obj_in: InvoiceCreate) -> Optional[Invoice]:
    insert_data = obj_in.dict(exclude_unset=True)
    obj_db = Invoice(**insert_data)
    async with db.obtain_session() as sess:
        sess.add(obj_db)
    return obj_db


async def update(obj_db: Invoice, obj_in: InvoiceUpdate) -> Invoice:
    obj_data = jsonable_encoder(obj_db)
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(obj_db, field, update_data[field])

    async with db.obtain_session() as sess:
        sess.add(obj_db)
    return obj_db


async def remove(id: int) -> Any:
    async with db.obtain_session() as sess:
        result = await sess.execute(delete(Invoice).where(Invoice.id == id))
    if result.rowcount == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f'Record with id={id} not found')
