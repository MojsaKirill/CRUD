import enum

from sqlalchemy import Column, Integer, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship

from db.session import Base


class Statuses(str, enum.Enum):
    progress = 'progress'
    accept = 'accept'
    reject = 'reject'


class Invoice(Base):
    __tablename__ = 'invoice'

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('person.id', ondelete='CASCADE'), nullable=False)
    currency_id = Column(Integer, ForeignKey('currency.id', ondelete='CASCADE'), nullable=False)
    curr_count = Column(Numeric(precision=10, scale=2), nullable=False, default=0)
    status = Column(Enum(Statuses, create_constraint=True, name='statuses'), nullable=False,
                    default=Statuses.progress)

    person = relationship('Person', back_populates='invoices', lazy='joined', innerjoin=False)
    currency = relationship('Currency', back_populates='invoices', lazy='joined', innerjoin=False)
