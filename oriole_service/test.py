from oriole_service.db import *
from dao import *
import mongomock
from mock import *
from pytest import *
from mockredis import *
from oriole_service.log import logger
from nameko.testing.services import worker_factory


class Mock_app(object):
    """ Mock app.

    Examples::

        from oriole_service.test import *
        app = Mock_app()
    """

    app_base = "oriole_service.app.App."
    log_base = "oriole_service.log.Log."
    log_method = "get"
    app_methods = ["rs", "db", "init"]

    def mongo(self):
        return mongomock.MongoClient().db.collection

    def rs(self):
        return mock_redis_client()

    def db(self):
        engine = create_engine('sqlite://')
        Base.metadata.create_all(engine)
        return sessionmaker(engine)()

    def init(self):
        return lambda self: None

    def create(self, name):
        self.service = worker_factory(name)
        return self.service

    def get_attr(self, attr):
        attr.side_effect = self.get_effect

    def get_effect(self, args):
        self.get_result = args

    def set_attr(self, attr, value):
        attr.return_value = value

    def start(self, patch):
        methods = [self.rs, self.db, self.init]
        methods_zip = zip(self.app_methods, methods)
        for app_method, method in methods_zip:
            patch.setattr(self.app_base + app_method, method())
        patch.setattr(self.log_base + self.log_method, self.mongo)


@fixture
def app(monkeypatch):
    """
    Mock app. 
    """

    _log = logger()
    _log.info('Mock app...')
    mock_app = Mock_app()
    mock_app.start(monkeypatch)

    return mock_app
