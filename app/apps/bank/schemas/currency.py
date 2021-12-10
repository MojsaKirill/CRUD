import datetime
import decimal

from pydantic import BaseModel, Field, validator


class CurrencyBase(BaseModel):
    code: str = Field(..., title='Код', min_length=3, max_length=3)
    rate: decimal.Decimal = Field(..., title='Курс', gt=0)
    date_start: datetime.date = Field(..., title='Дата')


class Currency(CurrencyBase):
    id: int = Field(..., title='ID')

    class Config:
        orm_mode = True


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(CurrencyBase):
    pass


class CurrencyFromDB(BaseModel):
    code: str = Field(..., title='Код')

    class Config:
        orm_mode = True
