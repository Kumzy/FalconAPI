# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def Project(Base):
    __tablename__ = 'project'

    id = Column(UUID, primary_key=True)
    name = Column(String,nullable=False)
    code = Column(String)

    #It tells python how to print the class, used for debugging
    def __repr__(self):
        return '<Project {0}>'.format(self.name)

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(Project).filter(Project.id == id).one()