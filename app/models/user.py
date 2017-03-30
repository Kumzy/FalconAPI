# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String, Integer,Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
import json
Base = declarative_base()



class User(Base):
    __tablename__ = 'user'

    id = Column('id', UUID, primary_key=True)
    firstname = Column('firstname', String)
    lastname = Column('lastname', String)

    #It tells python how to print the class, used for debugging
    def __repr__(self):
        return "<User(id='%s', name='%s', lastname='%s')>"% \
            (self.id, self.firstname, self.lastname)

    def __init__(self, id , firstname, lastname):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname

    def __json__(self):
        return ['id', 'firstname']

    @classmethod
    def get_id(cls):
        return cls.id

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(cls).filter(cls.id == id).one()

    @classmethod
    def find_update(cls, session, id, args):
        return session.query(cls).filter(cls.get_id() == id).update(args, synchronize_session=False)

    def to_dict(self):
        #data =   [{'id': row[0], 'name': row[1]} for row in user_dbs.fetchall()]
        #return data
       # data = [{'thing_id': row[0], 'thing_name': row[1]} for row in cursor.fetchall()]
        intersection = set(self.__tablename__.columns.keys()) & set(self.FIELDS)
        return dict(map(
            lambda key:
            (key,
             (lambda value: self.FIELDS[key](value) if value else None)
             (getattr(self, key))),
            intersection))

    FIELDS = {
        'id ' : str,
        'firstname': str,
        'lastname': str
    }

