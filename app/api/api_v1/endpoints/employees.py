from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import deps
from apps.ref.cruds.employee import create, get_list
from apps.ref.schemas.employee import Employee, EmployeeCreate

router = APIRouter()


@router.get('/', response_model=List[Employee])
def list_employees(db: Session = Depends(deps.get_db),
                   skip: int = 0, limit: int = 100) -> Any:
    results = get_list(db, skip, limit)
    return results


@router.post('/create', response_model=Employee)
def create_person(item: EmployeeCreate, db: Session = Depends(deps.get_db)) -> Any:
    result = create(db, item)
    return result
