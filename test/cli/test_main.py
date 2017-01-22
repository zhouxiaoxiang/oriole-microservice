import sys
from pytest import *
from mock import patch
from oriole_service.cli.main import main


@yield_fixture(autouse=True)
def fake_argv():
    with patch.object(sys, 'argv',
        [
            'oriole',
            'test',
        ]):
        yield


def test_run():
    with patch('oriole_service.cli.test.main') as run:
        main()
    assert run.call_count == 1
