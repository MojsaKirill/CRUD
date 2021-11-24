from typing import Optional

from pydantic import BaseModel


class EmployeeBase(BaseModel):
    tab_num: int
    person_id: Optional[int] = None


class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True


class EmployeeCreate(EmployeeBase):
    pass
