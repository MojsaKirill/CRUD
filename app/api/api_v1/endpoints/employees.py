from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import deps
from apps.ref.cruds.employee import create, get_list, get_by_id, update, delete
from apps.ref.schemas.employee import Employee, EmployeeCreate, EmployeeUpdate

router = APIRouter()


@router.get('/{obj_id}', response_model=Employee)
def get_employee_by_id(obj_id: int, db: Session = Depends(deps.get_db)) -> Any:
    result = get_by_id(db, obj_id)
    if not result:
        raise HTTPException(status_code=404, detail='Employee not found!')
    return result


@router.get('/', response_model=List[Employee])
def list_employees(db: Session = Depends(deps.get_db),
                   skip: int = 0, limit: int = 100) -> Any:
    results = get_list(db, skip, limit)
    return results


@router.post('/create', response_model=Employee)
def create_employee(item: EmployeeCreate, db: Session = Depends(deps.get_db)) -> Any:
    result = create(db, item)
    return result


@router.put('/{obj_id}', response_model=Employee)
def update_employee(obj_id: int, item: EmployeeUpdate, db: Session = Depends(deps.get_db)) -> Any:
    obj_db = get_by_id(db, obj_id)
    if not obj_db:
        raise HTTPException(status_code=404, detail='Employee not found!')
    result = update(db, obj_db, item)
    return result


@router.delete('/{obj_id}', response_model=Employee)
def delete_employee(obj_id: int, db: Session = Depends(deps.get_db)) -> Any:
    result = get_by_id(db, obj_id)
    if not result:
        raise HTTPException(status_code=404, detail='Employee not found!')
    result = delete(db, obj_id)
    return result
