from services.user.user import *
from oriole_service.test import *


@fixture
def service(app):
    service = app.create(UserService)
    service.add_user('God')
    return service


def test_add_user(service):
    user = service.db.query(Users).first()
    assert user.name == 'God'
