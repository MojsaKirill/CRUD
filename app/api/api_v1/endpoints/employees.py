from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import deps
from apps.ref import cruds
from apps.ref.schemas.employee import Employee, EmployeeCreate, EmployeeUpdate

router = APIRouter()


@router.get('/{obj_id}', response_model=Employee)
def get_employee_by_id(obj_id: int, db: Session = Depends(deps.get_db)) -> Any:
    result = cruds.employee.get(db=db, id=obj_id)
    if not result:
        raise HTTPException(status_code=404, detail='Employee not found!')
    return result


@router.get('/', response_model=List[Employee])
def list_employees(db: Session = Depends(deps.get_db),
                   skip: int = 0, limit: int = 100) -> Any:
    results = cruds.employee.get_list(db=db, skip=skip, limit=limit)
    return results


@router.post('/create', response_model=Employee)
def create_employee(item: EmployeeCreate, db: Session = Depends(deps.get_db)) -> Any:
    result = cruds.employee.create(db=db, obj_in=item)
    return result


@router.put('/{obj_id}', response_model=Employee)
def update_employee(obj_id: int, item: EmployeeUpdate, db: Session = Depends(deps.get_db)) -> Any:
    obj_db = cruds.employee.get(db=db, id=obj_id)
    if not obj_db:
        raise HTTPException(status_code=404, detail='Employee not found!')
    result = cruds.employee.update(db=db, obj_db=obj_db, obj_in=item)
    return result


@router.delete('/{obj_id}', response_model=Employee)
def delete_employee(obj_id: int, db: Session = Depends(deps.get_db)) -> Any:
    result = cruds.employee.get(db=db, id=obj_id)
    if not result:
        raise HTTPException(status_code=404, detail='Employee not found!')
    result = cruds.employee.delete(db=db, id=obj_id)
    return result
