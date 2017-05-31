""" Oriole-DB """

from sqlalchemy import Column, Integer, String, create_engine, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_, or_, distinct, func
from oriole_service.api import get_config

Base = declarative_base()


class Db:
    def __init__(self, base=Base, database="database"):
        self.conf = get_config()
        pool_size = int(self.conf.get("pool_size", 10))
        pool_recycle = int(self.conf.get("pool_recycle", 300))

        self.base = base
        self.bind = create_engine(
            self.conf.get(database),
            pool_size=pool_size,
            pool_recycle=pool_recycle)
        self.base.metadata.create_all(self.bind)

    def get_db(self):
        self.dbo = scoped_session(sessionmaker(self.bind))
        return self.dbo

    def rm_db(self):
        self.dbo.rollback()
        self.dbo.commit()
        self.dbo.close()
        self.base.metadata.drop_all(self.bind)
