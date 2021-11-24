from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import deps
from apps.ref.cruds.person import get_by_id, create, get_list, update, delete
from apps.ref.schemas.person import PersonCreate, Person, PersonUpdate

router = APIRouter()


@router.get('/{obj_id}', response_model=Person)
def get_person_by_id(obj_id: int, db: Session = Depends(deps.get_db)) -> Any:
    result = get_by_id(db, obj_id)
    if not result:
        raise HTTPException(status_code=404, detail='Person not found!')
    return result


@router.get('/', response_model=List[Person])
def list_persons(db: Session = Depends(deps.get_db),
                 skip: int = 0, limit: int = 100) -> Any:
    results = get_list(db, skip, limit)
    return results


@router.post('/create', response_model=Person)
def create_person(item: PersonCreate, db: Session = Depends(deps.get_db)) -> Any:
    result = create(db, item)
    return result


@router.put('/{obj_id}', response_model=Person)
def update_person(obj_id: int, item: PersonUpdate, db: Session = Depends(deps.get_db)) -> Any:
    obj_db = get_by_id(db, obj_id)
    if not obj_db:
        raise HTTPException(status_code=404, detail='Person not found!')
    result = update(db, obj_db, item)
    return result


@router.delete('/{obj_id}', response_model=Person)
def delete_person(obj_id: int, db: Session = Depends(deps.get_db)) -> Any:
    result = get_by_id(db, obj_id)
    if not result:
        raise HTTPException(status_code=404, detail='Person not found!')
    result = delete(db, obj_id)
    return result
