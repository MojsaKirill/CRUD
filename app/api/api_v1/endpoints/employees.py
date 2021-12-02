from typing import Any, List

from fastapi import APIRouter, HTTPException

from apps.ref import cruds
from apps.ref.schemas.employee import Employee, EmployeeCreate, EmployeeUpdate

router = APIRouter()


@router.get('/{obj_id}', response_model=Employee)
async def get_employee(obj_id: int) -> Any:
    result = await cruds.employee.get(id=obj_id)
    if not result:
        raise HTTPException(status_code=404, detail='Employee not found!')
    return result


@router.get('/', response_model=List[Employee])
async def list_employees(skip: int = 0, limit: int = 100) -> Any:
    results = await cruds.employee.get_list(skip=skip, limit=limit)
    return results


@router.post('/create', response_model=Employee, status_code=201)
async def create_employee(item: EmployeeCreate) -> Any:
    result = await cruds.employee.create(obj_in=item)
    return result


@router.put('/{obj_id}', response_model=Employee)
async def update_employee(obj_id: int, item: EmployeeUpdate) -> Any:
    obj_db = await cruds.employee.get(id=obj_id)
    if not obj_db:
        raise HTTPException(status_code=404, detail='Employee not found!')
    result = await cruds.employee.update(obj_db=obj_db, obj_in=item)
    return result


@router.delete('/{obj_id}')
async def delete_employee(obj_id: int) -> Any:
    result = await cruds.employee.delete(id=obj_id)
    return result
