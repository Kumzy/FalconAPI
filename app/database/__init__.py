# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import psycopg2
from app import config




def get_engine(uri):
    options = {
        'pool_recycle': 3600,
        'pool_size': 10,
        'pool_timeout': 30,
        'max_overflow': 30,
    }
    return create_engine(uri, **options)


db_session = scoped_session(sessionmaker())
engine = create_engine('postgresql+psycopg2://juliencourtes@localhost/falcon_api')


def init_session():
    db_session.configure(bind=engine)
"""s
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()
    Base.metadata.create_all(engine)"""

"""def init_session():
    engine = create_engine('postgresql+psycopg2://juliencourtes@localhost/falcon_api')
    session_sql = sessionmaker(bin=engine)
    Session = scoped_session(session_sql)"""