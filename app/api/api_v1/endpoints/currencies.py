from typing import Any, List

from fastapi import APIRouter

from apps.bank import cruds
from apps.bank.schemas.currency import Currency, CurrencyCreate

router = APIRouter()


@router.get('/', response_model=List[Currency])
async def list_currencies(skip: int = 0, limit: int = 100) -> Any:
    results = await cruds.currency.get_list(skip=skip, limit=limit)
    return results


@router.post('/create', response_model=Currency, status_code=201)
async def create_currency(item: CurrencyCreate) -> Any:
    result = await cruds.currency.create(obj_in=item)
    return result
