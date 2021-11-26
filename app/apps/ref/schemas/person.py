from typing import Optional

from pydantic import BaseModel, validator


class PersonBase(BaseModel):
    last_name: str
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    pers_num: Optional[str] = None

    @validator('pers_num')
    def pers_num_check(cls, v: str):
        if v:
            if len(v) != 14:
                raise ValueError('must be length 14 char')
        return v


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
    last_name: Optional[str] = None

    @validator('last_name')
    def last_name_check(cls, v: str):
        if v is None:
            raise ValueError('field required')
        return v
