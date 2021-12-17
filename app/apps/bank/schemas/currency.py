import datetime
import decimal

from pydantic import BaseModel, Field


class CurrencyBase(BaseModel):
    code: str = Field(..., title='Код', min_length=3, max_length=3)
    rate: decimal.Decimal = Field(..., title='Курс', gt=0)
    scale: int = Field(1, title='Шкала', ge=1)
    date_start: datetime.date = Field(..., title='Дата')


class CurrencyView(CurrencyBase):
    id: int = Field(..., title='ID')

    class Config:
        orm_mode = True


class CurrencyViewJoin(BaseModel):
    code: str = Field(..., title='Код')
    scale: int = Field(1, title='Шкала')
    rate: decimal.Decimal = Field(..., title='Курс')

    class Config:
        orm_mode = True


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(CurrencyBase):
    pass


class CurrencyRateOnDate(BaseModel):
    code: str = Field(..., title='Код', min_length=3, max_length=3)
    date_start: datetime.date = Field(..., title='Дата')
