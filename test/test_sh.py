from mock import patch
from pytest import *
from oriole_service.cli import setup_parser
from oriole_service.modules.sh import main


@fixture
def p():
    return setup_parser()


def test_sh(p):
    args = p.parse_args(['sh', ])

    with patch('oriole_service.api.remote_test') as run:
        main(args)
        assert run.call_count == 1


def test_sh(p):
    args = p.parse_args(['s', ])

    with patch('oriole_service.api.remote_test') as run:
        main(args)
        assert run.call_count == 1
