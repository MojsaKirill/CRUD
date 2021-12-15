from sqlalchemy import Column, Integer, Identity, String, Numeric, Boolean
from sqlalchemy.orm import relationship

from db.session import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Identity(always=True), primary_key=True)
    username = Column(String(70), nullable=False, unique=True, index=True)
    password = Column(String(100), nullable=False)
    email = Column(String(70), unique=True, nullable=True)
    balance = Column(Numeric(precision=10, scale=2), nullable=False, server_default='0')
    banker = Column(Boolean, nullable=False, server_default='False')

    invoices = relationship('Invoice', back_populates='user')
