from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from apps.ref.models.person import PersonTable
from apps.ref.schemas.person import PersonCreate, PersonUpdate


def get_by_id(db: Session, obj_id: int) -> PersonTable:
    person = db.query(PersonTable).get(obj_id)
    return person


def get_list(db: Session, skip: int = 0, limit: int = 100) -> List[PersonTable]:
    persons = db.query(PersonTable).offset(skip).limit(limit).all()
    return persons


def create(db: Session, obj_in: PersonCreate) -> PersonTable:
    data_in = jsonable_encoder(obj_in)
    db_obj = PersonTable(**data_in)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, obj_db: PersonTable, obj_in: PersonUpdate) -> PersonTable:
    data_obj = jsonable_encoder(obj_db)
    data_update = obj_in.dict(exclude_unset=True)
    for field in data_obj:
        if field in data_update:
            setattr(obj_db, field, data_update[field])
    db.add(obj_db)
    db.commit()
    db.refresh(obj_db)
    return obj_db


def delete(db: Session, obj_id: int) -> PersonTable:
    person = get_by_id(db, obj_id)
    db.delete(person)
    db.commit()
    return person
