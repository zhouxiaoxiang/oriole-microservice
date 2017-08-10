#
#                __   _,--="=--,_   __
#               /  \."    .-.    "./  \
#              /  ,/  _   : :   _  \/` \
#              \  `| /o\  :_:  /o\ |\__/
#               `-'| :="~` _ `~"=: |
#                  \`     (_)     `/
#           .-"-.   \      |      /   .-"-.
#    .-----{     }--|  /,.-'-.,\  |--{     }-----.
#     )    (_)_)_)  \_/`~-===-~`\_/  (_(_(_)    (
#    (                                          )
#     )                 Oriole-DB               (
#    (                  Eric.Zhou               )
#    '-------------------------------------------'
#

from sqlalchemy import Column, Integer, String, create_engine, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import and_, or_, distinct, func
from weakref import WeakKeyDictionary
from nameko.extensions import DependencyProvider
from redis import StrictRedis

Base = declarative_base()
RS_URI = "datasets"
DB_URI = "database"
DB_POOL = "pool_size"
DB_RECYCLE = "pool_recycle"


class Db(DependencyProvider):
    def __init__(self, Base):
        self.base = Base
        self.dbs = WeakKeyDictionary()

    def setup(self):
        self.conf = self.container.config
        pool_size = int(self.conf.get(DB_POOL, 10))
        pool_recycle = int(self.conf.get(DB_RECYCLE, 4 * 3600))

        self.bind = create_engine(
            self.conf.get(DB_URI),
            pool_size=pool_size,
            pool_recycle=pool_recycle)
        self.base.metadata.create_all(self.bind)

    def stop(self):
        self.bind.dispose()
        del self.bind

    def get_dependency(self, worker_ctx):
        session_cls = sessionmaker(self.bind)
        session = session_cls()
        self.dbs[worker_ctx] = session
        return session

    def worker_teardown(self, worker_ctx):
        session = self.dbs.pop(worker_ctx)
        session.close()


class Rs(DependencyProvider):
    def setup(self):
        self.conf = self.container.config
        self.rs = StrictRedis.from_url(self.conf.get(RS_URI))

    def get_dependency(self, worker_ctx):
        return self.rs
