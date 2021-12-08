from sqlalchemy import Column, Index, Integer, String, Numeric, Date

from db.session import Base


class Currency(Base):
    __table__ = 'currency'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(length=3), unique=True, index=True, nullable=False)
    rate = Column(Numeric(scale=10, precision=3), nullable=False)
    date = Column(Date, index=True, nullable=False)

    # Index('currency_uq01', Currency.code, )