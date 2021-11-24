from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from apps.ref.models.person import PersonTable, persons
from apps.ref.schemas.person import PersonCreate, PersonUpdate


def get_by_id(db: Session, obj_id: int) -> PersonTable:
    sql = select(PersonTable).where(PersonTable.id == obj_id)
    result = db.execute(sql).scalar_one_or_none()
    # result = db.query(PersonTable).get(obj_id)
    return result


def get_list(db: Session, skip: int = 0, limit: int = 100) -> List[PersonTable]:
    sql = select(PersonTable)
    # sql = sql.with_only_columns(persons.c.id, persons.c.last_name)
    # sql = sql.with_only_columns(PersonTable.id, PersonTable.last_name)
    sql = sql.offset(skip).limit(limit)
    print('SQL: ', sql)
    results = db.execute(sql).scalars().all()
    # results = db.query(PersonTable).offset(skip).limit(limit).all()
    return results


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
