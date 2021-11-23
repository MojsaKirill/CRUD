from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import deps
from apps.ref.cruds.person import get_by_id, create, get_list, update, delete
from apps.ref.models.person import PersonTable
from apps.ref.schemas.person import PersonCreate, Person, PersonUpdate

router = APIRouter()


@router.get('/', response_model=List[Person])
def list_persons(db: Session = Depends(deps.get_db),
                 skip: int = 0, limit: int = 100) -> Any:
    persons = get_list(db, skip, limit)
    return persons


@router.get('/{obj_id}', response_model=Person)
def get_person_by_id(obj_id: int, db: Session = Depends(deps.get_db)) -> Any:
    person = get_by_id(db, obj_id)
    if not person:
        raise HTTPException(status_code=404, detail='Person not found!')
    return person


@router.post('/create', response_model=Person)
def create_person(item: PersonCreate, db: Session = Depends(deps.get_db)) -> Any:
    person = create(db, item)
    return person


@router.put('/{obj_id}', response_model=Person)
def update_person(obj_id: int, item: PersonUpdate, db: Session = Depends(deps.get_db)) -> Any:
    obj_db = get_by_id(db, obj_id)
    if not obj_db:
        raise HTTPException(status_code=404, detail='Person not found!')
    person = update(db, obj_db, item)
    return person


@router.delete('/{obj_id}', response_model=Person)
def delete_person(obj_id: int, db: Session = Depends(deps.get_db)) -> Any:
    person = get_by_id(db, obj_id)
    if not person:
        raise HTTPException(status_code=404, detail='Person not found!')
    person = delete(db, obj_id)
    return person
