""" Oriole-DB """

from sqlalchemy import Column, Integer, String, create_engine, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_, or_, distinct, func
from redis import StrictRedis
from oriole_service.api import Config

Base = declarative_base()


class Db(object):
    def __init__(self, base=Base, database="database"):
        self.base = base
        self.engine = create_engine(Config().get(database))
        self.base.metadata.create_all(self.engine)
        self.session = scoped_session(sessionmaker(self.engine))

    def get_db(self):
        self.dbo = self.session()
        return self.dbo

    def rm_db(self):
        self.dbo.rollback()
        self.dbo.commit()
        self.dbo.close()
        self.base.metadata.drop_all(self.engine)
        self.engine.dispose()

    @staticmethod
    def get_rs():
        return StrictRedis.from_url(Config()["datasets"])
