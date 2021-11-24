from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import select
from sqlalchemy.orm import Session

from apps.ref.models.employee import EmployeeTable, employees
from apps.ref.models.person import PersonTable, persons
from apps.ref.schemas.employee import EmployeeCreate


def get_list(db: Session, skip: int = 0, limit: int = 100) -> List[EmployeeTable]:
    # sql = select(employees).outerjoin(persons).add_column(persons.c.last_name)
    # print('SQL: ', sql)
    # sql = sql.with_only_columns(persons.c.id, persons.c.last_name)
    # sql = sql.with_only_columns(PersonTable.id, PersonTable.last_name)
    # sql = sql.offset(skip).limit(limit)
    # results = db.execute(sql).scalars().all()
    results = db.query(EmployeeTable).offset(skip).limit(limit).all()
    return results


def create(db: Session, obj_in: EmployeeCreate) -> EmployeeTable:
    data_in = jsonable_encoder(obj_in)
    db_obj = EmployeeTable(**data_in)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
