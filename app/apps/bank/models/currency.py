from sqlalchemy import Column, Index, Integer, String, Numeric, Date, UniqueConstraint

from db.session import Base


class Currency(Base):
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(length=3), nullable=False)
    rate = Column(Numeric(scale=10, precision=3), nullable=False)
    date = Column(Date, nullable=False)

    # __table_args__ = (Index('currency_uq01', 'code', 'date', unique=True),)


Index('currency_uq01', Currency.code, Currency.date, unique=True)
