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
#    (                                           )
#     )                Oriole-TEST              (
#    (                  Eric.Zhou                )
#    '-------------------------------------------'
#

from mock import *
from nameko.testing.services import worker_factory
from pytest import *

from dao import *
from oriole.fake import fake_db, fake_mongo, fake_redis


@yield_fixture
def app(monkeypatch):
    class _App:
        def __init__(self, fake):
            self.fake = fake.setattr
            self._db = fake_db(Base)
            self.dbs = [self._db]

            for old, new in zip((
                "oriole_service.app.App.rs",
                "oriole_service.app.App.db",
            ), (fake_redis(), self._db.get())):
                self.fake(old, new)

        def close(self):
            for db in self.dbs:
                db.close()

        def create(self, name):
            return worker_factory(name)

        def add_db(self, service, name='db', uri='test_database', base=Base):
            db = fake_db(base, uri)
            self.dbs.append(db)
            self.fake(service, name, db.get())

        def add_mongo(self, service, name='db_log'):
            self.fake(service, name, fake_mongo())

    # Supply database and redis to test.
    _app = _App(monkeypatch)

    # Only supply app to create service.
    # Don't create service by class directly, it's wrong.
    yield _app
    _app.close()
