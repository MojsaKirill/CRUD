from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.session import Base


class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(length=100), doc='doc', comment='comment')
    first_name = Column(String(length=100), nullable=True)
    middle_name = Column(String(length=100), nullable=True)
    name_lfm = Column(String(length=150), nullable=True, index=True)
    name_fml = Column(String(length=150), nullable=True, index=True)
    pers_num = Column(String(length=14), unique=True, index=True)

    employees = relationship('Employee', back_populates='person')


persons = Person.__table__
