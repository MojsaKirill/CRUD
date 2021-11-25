from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, validates

from core.utils import get_lfm
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

    @validates('last_name', 'first_name', 'middle_name')
    def convert_title(self, key, value: str):
        if value:
            return value.title()
        else:
            if key == 'last_name':
                raise ValueError('Not null')
        return value

    @validates('name_lfm')
    def gen_lfm(self, key, value: str):
        print('value: ', value)
        return get_lfm(self.last_name, self.first_name, self.middle_name)

    # @hybrid_property
    # def name_lfm(self):
    #     return self._name_lfm

    # @name_lfm.setter
    # def name_lfm(self, value: str):
    #     print(value)
    #     self._name_lfm = get_lfm(self.last_name, self.first_name, self.middle_name)


persons = Person.__table__
