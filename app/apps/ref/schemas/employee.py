from typing import Optional

from pydantic import BaseModel

from apps.ref.schemas.person import Person


class EmployeeBase(BaseModel):
    tab_num: int
    person_id: Optional[int] = None


class Employee(EmployeeBase):
    id: int
    person: Optional[Person] = None

    class Config:
        orm_mode = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass
