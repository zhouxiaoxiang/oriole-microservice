from sqlalchemy import Column, Integer, String, create_engine, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_, or_, distinct, func
from redis import StrictRedis
from oriole_service.conf import Config
from oriole_service.log import logger

Base = declarative_base()


class Db(object):
    """ Create db.

    Examples::

        from oriole_service.db import *
        db = Db()
        db.get_db()
        db.get_rs()
    """

    def __init__(self, base=Base):
        self.base = base
        self._log = logger()
        self.config = Config()

    def get_db(self):
        self._log.info("Get db...")
        self.engine = create_engine(self.config["database"])
        self.base.metadata.create_all(self.engine)
        return scoped_session(sessionmaker(self.engine))

    def drop_db(self):
        self._log.info("Drop db...")
        self.base.metadata.drop_all(self.engine)

    def get_rs(self):
        self._log.info("Get redis...")
        return StrictRedis.from_url(self.config["datasets"])
