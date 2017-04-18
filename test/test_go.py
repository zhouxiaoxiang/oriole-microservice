from mock import patch
from pytest import *
from oriole_service.cli import setup_parser
from oriole_service.modules.go import main


@fixture
def p():
    return setup_parser()


def test_go(p):
    args = p.parse_args([
        'go',
        'log',
    ])

    with patch('oriole_service.api.copy') as run:
        main(args)
        assert run.call_count == 1
        assert run.call_args[0][1] == 'log'


def test_g(p):
    args = p.parse_args([
        'g',
        'log',
    ])

    with patch('oriole_service.api.copy') as run:
        main(args)
        assert run.call_count == 1
        assert run.call_args[0][1] == 'log'
