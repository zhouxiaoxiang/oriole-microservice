""" Oriole-DB """

from sqlalchemy import Column, Integer, String, create_engine, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_, or_, distinct, func
from redis import StrictRedis
from oriole_service.api import Config

Base = declarative_base()


class Db(object):
    def __init__(self, base=Base):
        self.engine = ""
        self.base = base
        self.config = Config()

    def get_db(self):
        database = self.config.get("database")
        return self.create_db(database)

    def get_test_db(self):
        database = self.config.get("test_database", "sqlite://")
        return self.create_db(database)

    def drop_db(self):
        self.dbo.rollback()
        self.dbo.commit()
        self.dbo.close()
        self.base.metadata.drop_all(self.engine)
        self.engine.dispose()

    def get_rs(self):
        return StrictRedis.from_url(self.config["datasets"])

    def create_db(self, database):
        self.engine = create_engine(database)
        self.base.metadata.create_all(self.engine)
        self.dbo = scoped_session(sessionmaker(self.engine))
        return self.dbo
