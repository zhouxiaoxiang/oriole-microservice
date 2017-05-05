from mock import patch
from pytest import *
from oriole_service.cli import setup_parser
from oriole_service.modules.test import main


@fixture
def p():
    return setup_parser()


def test_test(p):
    args = p.parse_args([
        'test',
        'log',
    ])

    with patch('oriole_service.api.mexe') as run:
        main(args)
        assert run.call_count == 1
        assert 'log' in run.call_args[0][1]


def test_t(p):
    args = p.parse_args([
        't',
        'log',
    ])

    with patch('oriole_service.api.mexe') as run:
        main(args)
        assert run.call_count == 1
        assert 'log' in run.call_args[0][1]
