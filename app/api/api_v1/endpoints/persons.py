from typing import Any, List, Optional

from fastapi import APIRouter, HTTPException

from apps.ref import cruds
from apps.ref.schemas.person import Person, PersonCreate, PersonUpdate

router = APIRouter()


@router.get('/{obj_id}', response_model=Person)
async def get_person(obj_id: int) -> Any:
    result = await cruds.person.get(id=obj_id)
    if not result:
        raise HTTPException(status_code=404, detail='Person not found!')
    return result


@router.get('/', response_model=List[Person])
async def list_persons(q: Optional[str] = None, skip: int = 0, limit: int = 100) -> Any:
    results = await cruds.person.get_list(q, skip=skip, limit=limit)
    return results


@router.post('/create', response_model=Person, status_code=201)
async def create_person(item: PersonCreate) -> Any:
    result = await cruds.person.create_invoice(obj_in=item)
    return result


@router.put('/{obj_id}', response_model=Person)
async def update_person(obj_id: int, item: PersonUpdate) -> Any:
    obj_db = await cruds.person.get(id=obj_id)
    if not obj_db:
        raise HTTPException(status_code=404, detail='Person not found!')
    result = await cruds.person.update_invoice(obj_db=obj_db, obj_in=item)
    return result


@router.delete('/{obj_id}')
async def delete_person(obj_id: int) -> Any:
    result = await cruds.person.delete(id=obj_id)
    return result
