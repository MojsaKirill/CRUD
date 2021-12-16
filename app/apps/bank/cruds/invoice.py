from typing import Any, List, Optional, Union, Dict

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, insert, and_, update
from starlette import status
from starlette.responses import JSONResponse

from apps.auth.model import User
from apps.bank.models.invoice import Invoice, Statuses
from apps.bank.schemas.invoice import InvoiceCreate, InvoiceUpdate
from core.exceptions import invoice_change_exception
from core.utils import obj_to_dict
from db.session import SessionManager

db = SessionManager()


async def get(id: Any, user: User) -> Optional[Invoice]:
    select_stmt = select(Invoice)
    if not user.banker:
        select_stmt = select_stmt.where(Invoice.user_id == user.id)
    select_stmt = select_stmt.where(Invoice.id == id)
    async with db.obtain_session() as sess:
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def get_list(user: User = None,
                   skip: int = 0,
                   limit: int = 100) -> List[Invoice]:
    select_stmt = select(Invoice)
    if user:
        if user.banker:
            select_stmt = select_stmt.where(Invoice.status == Statuses.progress)
        else:
            select_stmt = select_stmt.where(Invoice.user_id == user.id)
    select_stmt = select_stmt.offset(skip).limit(limit)
    async with db.obtain_session() as sess:
        results = (await sess.execute(select_stmt)).scalars().all()
    return results


async def create_invoice(obj_in: Union[InvoiceCreate, Dict[str, Any]],
                         user: User) -> Optional[Invoice]:
    insert_data = obj_to_dict(obj_in)
    insert_data['user_id'] = user.id
    async with db.obtain_session() as sess:
        insert_stmt = insert(Invoice).values(**insert_data).returning(Invoice)
        result = (await sess.execute(insert_stmt)).mappings().first()
    return result


async def update_invoice(obj_db: Invoice, obj_in: Union[InvoiceUpdate, Dict[str, Any]],
                         user: User) -> Invoice:
    if obj_db.status != Statuses.progress:
        raise invoice_change_exception
    if not user.banker and obj_db.user_id != user.id:
        raise invoice_change_exception

    update_data = obj_to_dict(obj_in)
    update_stmt = update(Invoice).where(Invoice.id == obj_db.id).values(**update_data)
    update_stmt = update_stmt.returning(Invoice)
    async with db.obtain_session() as sess:
        result = (await sess.execute(update_stmt)).mappings().first()
    return result


async def remove(id: int, user: User) -> Any:
    async with db.obtain_session() as sess:
        result = await sess.execute(delete(Invoice).where(and_(
            Invoice.id == id,
            Invoice.user_id == user.id,
            Invoice.status == Statuses.progress
        )))
    if result.rowcount == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f'Record with id={id} not found')
