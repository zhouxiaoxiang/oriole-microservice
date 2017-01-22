from services.log.log import *
from oriole_service.test import *


@fixture
def service(app):
    return app.create(LogService)


def test_add_log(service):
    log = {"content": "info"}
    service.add_log(log)
    result = service.log.find_one(log)
    assert result["content"] == "info" 
