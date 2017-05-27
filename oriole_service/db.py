""" Oriole-DB """

from sqlalchemy import Column, Integer, String, create_engine, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_, or_, distinct, func
from redis import StrictRedis
from oriole_service.api import Config

Base = declarative_base()


class Db:
    def __init__(self, base=Base, database="database"):
        self.base = base
        self.conf = Config()
        self.bind = create_engine(self.conf.get(database), pool_recycle=3600)
        self.base.metadata.create_all(self.bind)
        self.dbs = scoped_session(sessionmaker(self.bind))

    def get_db(self):
        self.dbo = self.dbs()
        return self.dbo

    def rm_db(self):
        self.dbo.rollback()
        self.dbo.commit()
        self.dbo.close()
        self.base.metadata.drop_all(self.bind)
        self.bind.dispose()

    def get_rs(self):
        return StrictRedis.from_url(self.conf.get("datasets"))
