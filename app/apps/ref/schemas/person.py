from typing import Optional, List

from pydantic import BaseModel


class PersonBase(BaseModel):
    last_name: str
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    pers_num: Optional[str] = None


class Person(PersonBase):
    id: int
    name_lfm: Optional[str] = None
    name_fml: Optional[str] = None

    class Config:
        orm_mode = True


class PersonCreate(PersonBase):
    pass


class PersonUpdate(PersonBase):
    pass
