from typing import Any, List

from fastapi import APIRouter, HTTPException

from apps.bank.cruds import currency
from apps.bank.schemas.currency import CurrencyCreate, CurrencyUpdate, CurrencyView

router = APIRouter()


@router.get('/{obj_id}', response_model=CurrencyView)
async def get_currency(obj_id: int) -> Any:
    result = await currency.get(id=obj_id)
    if not result:
        raise HTTPException(status_code=404, detail='Currency not found!')
    return result


@router.get('/', response_model=List[CurrencyView])
async def list_currencies(skip: int = 0, limit: int = 100) -> Any:
    results = await currency.get_list(skip=skip, limit=limit)
    return results


@router.post('/create', response_model=CurrencyView, status_code=201)
async def create_currency(item: CurrencyCreate) -> Any:
    result = await currency.create(obj_in=item)
    return result


@router.put('/{obj_id}', response_model=CurrencyView)
async def update_currency(obj_id: int, item: CurrencyUpdate) -> Any:
    obj_db = await currency.get(id=obj_id)
    if not obj_db:
        raise HTTPException(status_code=404, detail='Currency not found!')
    result = await currency.update(obj_db=obj_db, obj_in=item)
    return result


@router.delete('/{obj_id}')
async def delete_currency(obj_id: int) -> Any:
    result = await currency.remove(id=obj_id)
    return result
