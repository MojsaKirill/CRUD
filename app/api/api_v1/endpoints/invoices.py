from typing import Any, List

from fastapi import APIRouter, HTTPException

from apps.bank.cruds import invoice
from apps.bank.schemas.invoice import InvoiceUpdate, InvoiceView, InvoiceCreate, InvoiceFromDB

router = APIRouter()


@router.get('/{obj_id}', response_model=InvoiceFromDB)
async def get_invoice(obj_id: int) -> Any:
    result = await invoice.get(id=obj_id)
    if not result:
        raise HTTPException(status_code=404, detail='Invoice not found!')
    return result


@router.get('/', response_model=List[InvoiceFromDB])
async def list_invoices(skip: int = 0, limit: int = 100) -> Any:
    results = await invoice.get_list(skip=skip, limit=limit)
    return results


@router.post('/create', response_model=InvoiceView, status_code=201)
async def create_invoice(item: InvoiceCreate) -> Any:
    result = await invoice.create(obj_in=item)
    return result


@router.put('/{obj_id}', response_model=InvoiceView)
async def update_invoice(obj_id: int, item: InvoiceUpdate) -> Any:
    obj_db = await invoice.get(id=obj_id)
    if not obj_db:
        raise HTTPException(status_code=404, detail='Invoice not found!')
    result = await invoice.update(obj_db=obj_db, obj_in=item)
    return result


@router.delete('/{obj_id}')
async def delete_invoice(obj_id: int) -> Any:
    result = await invoice.remove(id=obj_id)
    return result
