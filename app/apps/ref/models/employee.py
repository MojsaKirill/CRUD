from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.session import Base


class EmployeeTable(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tab_num = Column(Integer, unique=True, nullable=False)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete='SET NULL'), nullable=True)
    # person = relationship('Person', back_populates='employees')


employees = EmployeeTable.__table__
