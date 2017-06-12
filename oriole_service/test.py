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
#     )                Oriole-TEST              (
#    (                  Eric.Zhou               )
#    '-------------------------------------------'
#

from oriole_service.db import *
from dao import *
import mongomock
from mock import *
from pytest import *
from mockredis import *
from nameko.testing.services import worker_factory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from oriole_service.api import get_config


@fixture
def app(monkeypatch):
    class _Base:
        """ App interface """

        def duck(self, patch):
            app_base = "oriole_service.app.App."
            log_base = "oriole_service.log.Log."
            log_method = "get"
            methods = ["rs", "db", "init"]

            for old, new in zip(methods, [self.rs, self.db, self.init]):
                patch.setattr(app_base + old, new())
            patch.setattr(log_base + log_method, self.mongo)

        def create(self, name):
            return worker_factory(name)

    class App(_Base):
        """ Supply database """

        def __init__(self, patch):
            self.duck(patch)

        def init(self):
            return lambda self: None

        def mongo(self):
            return mongomock.MongoClient().db.collection

        def rs(self):
            return mock_redis_client()

        def db(self):
            self.bind = create_engine(get_config().get("test_database"))
            Base.metadata.create_all(self.bind)
            session_cls = sessionmaker(self.bind)
            self.session = session_cls()

            return self.session

        def close(self):
            self.session.rollback()
            self.session.commit()
            self.session.close()
            Base.metadata.drop_all(self.bind)
            self.bind.dispose()

    # Supply database and redis to test.
    _app = App(monkeypatch)

    # Only supply app to create service.
    # Don't create service by class directly, it's wrong.
    yield _app
    _app.close()
