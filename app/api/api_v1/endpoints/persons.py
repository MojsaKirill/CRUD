from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import deps
from apps.ref.models.person import PersonTable
from apps.ref.schemas.person import PersonCreate, Person

router = APIRouter()


@router.get('/', response_model=List[Person])
def list_persons(db: Session = Depends(deps.get_db),
                 skip: int = 0, limit: int = 100, ):
    return db.query(PersonTable).offset(skip).limit(limit).all()


@router.post('/create')
def create_person(item: PersonCreate, db: Session = Depends(deps.get_db)):
    person = PersonTable(**item.dict())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person
