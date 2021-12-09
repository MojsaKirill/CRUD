from typing import Optional

from pydantic import BaseModel, Field

from apps.ref.schemas.person import Person, PersonFromDB


class EmployeeBase(BaseModel):
    tab_num: int = Field(..., title='Табельный номер')
    person_id: int = Field(None, title='Код персоны')


class Employee(EmployeeBase):
    id: int = Field(..., title='Код')
    person: PersonFromDB = Field(None, title='Персона')
    # person: Person.value['']

    class Config:
        orm_mode = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeFromDB(EmployeeBase):
    id: int = Field(..., title='Код')
