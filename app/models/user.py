# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def User(Base):
    __tablename__= 'user'

    id = Column(UUID, primary_key=True)
    firstname = Column(String,nullable=False)
    lastname = Column(String,nullable=False)

    #It tells python how to print the class, used for debugging
    def __repr__(self):
        return '<User {0}>'.format(self.firsname + ' '+self.lastname)

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(User).filter(User.id == id).one()