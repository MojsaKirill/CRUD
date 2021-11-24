from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from apps.ref.models.person import Person, persons
from apps.ref.schemas.person import PersonCreate, PersonUpdate


def get_by_id(db: Session, obj_id: int) -> Person:
    sql = select(Person).where(Person.id == obj_id)
    result = db.execute(sql).scalar_one_or_none()
    # result = db.query(Person).get(obj_id)
    return result


def get_list(db: Session, skip: int = 0, limit: int = 100) -> List[Person]:
    sql = select(Person).offset(skip).limit(limit)
    results = db.execute(sql).scalars().all()
    # results = db.query(Person).offset(skip).limit(limit).all()
    return results


def create(db: Session, obj_in: PersonCreate) -> Person:
    data_in = jsonable_encoder(obj_in)
    obj_db = Person(**data_in)
    db.add(obj_db)
    db.commit()
    db.refresh(obj_db)
    return obj_db


def update(db: Session, obj_db: Person, obj_in: PersonUpdate) -> Person:
    data_obj = jsonable_encoder(obj_db)
    data_update = obj_in.dict(exclude_unset=True)
    for field in data_obj:
        if field in data_update:
            setattr(obj_db, field, data_update[field])
    db.add(obj_db)
    db.commit()
    db.refresh(obj_db)
    return obj_db


def delete(db: Session, obj_id: int) -> Person:
    person = get_by_id(db, obj_id)
    db.delete(person)
    db.commit()
    return person
