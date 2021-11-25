from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import deps
from apps.ref import cruds
from apps.ref.schemas.person import Person, PersonCreate, PersonUpdate

router = APIRouter()


@router.get('/{obj_id}', response_model=Person)
def get_person_by_id(obj_id: int, db: Session = Depends(deps.get_db)) -> Any:
    result = cruds.person.get(db=db, id=obj_id)
    if not result:
        raise HTTPException(status_code=404, detail='Person not found!')
    return result


@router.get('/', response_model=List[Person])
def list_persons(db: Session = Depends(deps.get_db),
                 skip: int = 0, limit: int = 100) -> Any:
    results = cruds.person.get_list(db=db, skip=skip, limit=limit)
    return results


@router.post('/create', response_model=Person)
def create_person(item: PersonCreate, db: Session = Depends(deps.get_db)) -> Any:
    result = cruds.person.create(db=db, obj_in=item)
    return result


@router.put('/{obj_id}', response_model=Person)
def update_person(obj_id: int, item: PersonUpdate, db: Session = Depends(deps.get_db)) -> Any:
    obj_db = cruds.person.get(db=db, id=obj_id)
    if not obj_db:
        raise HTTPException(status_code=404, detail='Person not found!')
    result = cruds.person.update(db=db, obj_db=obj_db, obj_in=item)
    return result


@router.delete('/{obj_id}', response_model=Person)
def delete_person(obj_id: int, db: Session = Depends(deps.get_db)) -> Any:
    result = cruds.person.get(db=db, id=obj_id)
    if not result:
        raise HTTPException(status_code=404, detail='Person not found!')
    result = cruds.person.delete(db=db, id=obj_id)
    return result
