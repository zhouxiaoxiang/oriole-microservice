""" Oriole-TEST """

from oriole_service.db import *
from dao import *
import mongomock
from mock import *
from pytest import *
from mockredis import *
from oriole_service.log import logger
from nameko.testing.services import worker_factory


@fixture
def app(monkeypatch):
    class _Base(object):
        """ App interface """

        app_base = "oriole_service.app.App."
        log_base = "oriole_service.log.Log."
        log_method = "get"
        app_methods = ["rs", "db", "init"]

        def get_attr(self, attr):
            attr.side_effect = self.get_effect

        def get_effect(self, args):
            self.get_result = args

        def set_attr(self, attr, value):
            attr.return_value = value

        def duck(self, patch):
            for app_method, method in zip(self.app_methods,
                                          [self.rs, self.db, self.init]):
                patch.setattr(self.app_base + app_method, method())
            patch.setattr(self.log_base + self.log_method, self.mongo)

        def close(self):
            self.eng.drop_db()

        def create(self, name):
            return worker_factory(name)

    class App(_Base):
        """ Supply database """

        def __init__(self, patch):
            self.duck(patch)

        def mongo(self):
            return mongomock.MongoClient().db.collection

        def rs(self):
            return mock_redis_client()

        def db(self):
            self.eng = Db(Base)
            self.dbo = self.eng.get_test_db()
            return self.dbo

        def init(self):
            return lambda self: None

    _app = App(monkeypatch)
    yield _app
    _app.close()
