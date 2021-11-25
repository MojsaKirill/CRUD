from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, validates

from core.utils import get_lfm, get_fml
from db.session import Base


def gen_name_lfm(context):
    print('Context: ', context.get_current_parameters())
    return get_lfm(context.get_current_parameters()['last_name'],
                   context.get_current_parameters()['first_name'],
                   context.get_current_parameters()['middle_name'])


def gen_name_fml(context):
    return get_fml(context.get_current_parameters()['last_name'],
                   context.get_current_parameters()['first_name'],
                   context.get_current_parameters()['middle_name'])


class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(length=100), nullable=False)
    first_name = Column(String(length=100), nullable=True)
    middle_name = Column(String(length=100), nullable=True)
    name_lfm = Column(String(length=150),
                      default=gen_name_lfm, onupdate=gen_name_lfm, index=True)
    name_fml = Column(String(length=150),
                      default=gen_name_fml, onupdate=gen_name_fml, index=True)
    pers_num = Column(String(length=14), nullable=True, unique=True, index=True)

    employees = relationship('Employee', back_populates='person')

    @validates('last_name', 'first_name', 'middle_name')
    def convert_title(self, key, value: str):
        if value:
            return value.title()
        else:
            if key == 'last_name':
                raise ValueError('Not null')
        return value

    # @validates('name_lfm')
    # def gen_lfm(self, key, value: str):
    #     print('value: ', value)
    #     return get_lfm(self.last_name, self.first_name, self.middle_name)

    # @hybrid_property
    # def name_lfm(self):
    #     return self._name_lfm

    # @name_lfm.setter
    # def name_lfm(self, value: str):
    #     print(value)
    #     self._name_lfm = get_lfm(self.last_name, self.first_name, self.middle_name)


persons = Person.__table__
