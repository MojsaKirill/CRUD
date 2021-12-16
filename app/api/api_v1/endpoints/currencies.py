import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from apps.bank.cruds import currency
from apps.bank.schemas.currency import CurrencyCreate, CurrencyRateOnDate, CurrencyUpdate, \
    CurrencyView
from core.security import current_user_is_banker

router = APIRouter()


@router.get('/', response_model=List[CurrencyView])
async def list_currencies(skip: int = 0, limit: int = 100) -> Any:
    results = await currency.get_list(skip=skip, limit=limit)
    return results


@router.get('/{code}/{date}', response_model=CurrencyView)
async def get_code_rate(code: str, date: datetime.date) -> Any:
    curr_rate = CurrencyRateOnDate(code=code, date_start=date)
    result = await currency.get_code_rate_on_date(curr_rate)
    return result


@router.get('/{obj_id}', response_model=CurrencyView)
async def get_currency(obj_id: int) -> Any:
    result = await currency.get(id=obj_id)
    if not result:
        raise HTTPException(status_code=404, detail='Currency not found!')
    return result


@router.post('/create', response_model=CurrencyView, status_code=201,
             dependencies=[Depends(current_user_is_banker)])
async def create_currency(item: CurrencyCreate) -> Any:
    result = await currency.create_currency(obj_in=item)
    return result


@router.put('/{obj_id}', response_model=CurrencyView,
            dependencies=[Depends(current_user_is_banker)])
async def update_currency(obj_id: int, item: CurrencyUpdate) -> Any:
    obj_db = await currency.get(id=obj_id)
    if not obj_db:
        raise HTTPException(status_code=404, detail='Currency not found!')
    result = await currency.update_currency(obj_db=obj_db, obj_in=item)
    return result


@router.delete('/{obj_id}', dependencies=[Depends(current_user_is_banker)])
async def delete_currency(obj_id: int) -> Any:
    result = await currency.remove_currency(id=obj_id)
    return result
