from typing import Optional

from pydantic import BaseModel, Field, validator


class PersonBase(BaseModel):
    last_name: str = Field(..., title='Фамилия', min_length=3, max_length=100)
    first_name: str = Field(None, title='Имя', max_length=100)
    middle_name: str = Field(None, title='Отчество', max_length=100)
    pers_num: str = Field(None, title='Личный номер', min_length=14, max_length=14)


class Person(PersonBase):
    id: int = Field(..., title='Код')
    name_lfm: str = Field(None, title='Фамилия И.О.')
    name_fml: str = Field(None, title='И.О. Фамилия')

    class Config:
        orm_mode = True


class PersonCreate(PersonBase):
    pass


class PersonUpdate(PersonBase):
    pass
    last_name: str = Field(None, title='Фамилия', min_length=3, max_length=100)

    @validator('last_name')
    def last_name_check(cls, v: str):
        if v is None:
            raise ValueError('field required')
        return v


class PersonFromDB(BaseModel):
    # id: int = Field(..., title='Код')
    pers_num: str = Field(None, title='Личный номер')
    # last_name: str = Field(..., title='Фамилия')
    # first_name: str = Field(None, title='Имя')
    # middle_name: str = Field(None, title='Отчество')
    name_lfm: str = Field(None, title='Фамилия И.О.')
    # name_fml: str = Field(None, title='И.О. Фамилия')

    class Config:
        orm_mode = True
