"""
                __   _,--="=--,_   __
               /  \."    .-.    "./  \
              /  ,/  _   : :   _  \/` \
              \  `| /o\  :_:  /o\ |\__/
               `-'| :="~` _ `~"=: |
                  \`     (_)     `/
           .-"-.   \      |      /   .-"-.
    .-----{     }--|  /,.-'-.,\  |--{     }-----.
     )    (_)_)_)  \_/`~-===-~`\_/  (_(_(_)    (
    (                                          )
     )                 Oriole-DB               (
    (                  Eric.Zhou               )
    '-------------------------------------------'
"""

from sqlalchemy import Column, Integer, String, create_engine, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_, or_, distinct, func
from weakref import WeakKeyDictionary
from nameko.extensions import DependencyProvider

Base = declarative_base()
DB_URI = "database"


class Db(DependencyProvider):
    """Add sqlalchemy.

    It works for mysql and sqlite.
    """

    def __init__(self, Base):
        self.base = Base
        self.dbs = WeakKeyDictionary()

    def setup(self):
        """Setup sqlalchemy's pool.

        It's enough. Usually, active size is 2.
        """

        self.conf = self.container.config
        pool_size = int(self.conf.get("pool_size", 10))
        pool_recycle = int(self.conf.get("pool_recycle", 300))

        self.bind = create_engine(
            self.conf.get(DB_URI),
            pool_size=pool_size,
            pool_recycle=pool_recycle)
        self.base.metadata.create_all(self.bind)

    def stop(self):
        """Only a common usage, is not necessary. """

        self.bind.dispose()
        del self.bind

    def get_dependency(self, worker_ctx):
        """Supply a session to user. """

        session_cls = sessionmaker(self.bind)
        session = session_cls()
        self.dbs[worker_ctx] = session
        return session

    def worker_teardown(self, worker_ctx):
        """Don't store any session. """

        session = self.dbs.pop(worker_ctx)
        session.close()
