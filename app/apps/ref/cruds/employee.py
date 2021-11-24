from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import select
from sqlalchemy.orm import Session

from apps.ref.models.employee import Employee
from apps.ref.schemas.employee import EmployeeCreate, EmployeeUpdate


def get_by_id(db: Session, obj_id: int) -> Employee:
    sql = select(Employee).where(Employee.id == obj_id)
    result = db.execute(sql).scalar_one_or_none()
    # result = db.query(Employee).get(obj_id)
    return result


def get_list(db: Session, skip: int = 0, limit: int = 100) -> List[Employee]:
    sql = select(Employee).offset(skip).limit(limit)
    results = db.execute(sql).scalars().all()
    # results = db.query(Employee).offset(skip).limit(limit).all()
    return results


def create(db: Session, obj_in: EmployeeCreate) -> Employee:
    data_in = jsonable_encoder(obj_in)
    obj_db = Employee(**data_in)
    db.add(obj_db)
    db.commit()
    db.refresh(obj_db)
    return obj_db


def update(db: Session, obj_db: Employee, obj_in: EmployeeUpdate) -> Employee:
    data_obj = jsonable_encoder(obj_db)
    data_update = obj_in.dict(exclude_unset=True)
    for field in data_obj:
        if field in data_update:
            setattr(obj_db, field, data_update[field])
    db.add(obj_db)
    db.commit()
    db.refresh(obj_db)
    return obj_db


def delete(db: Session, obj_id: int) -> Employee:
    item = get_by_id(db, obj_id)
    db.delete(item)
    db.commit()
    return item
