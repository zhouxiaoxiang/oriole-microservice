from mock import patch
from pytest import *
from oriole_service.cli import setup_parser
from oriole_service.modules.doc import main


@fixture
def p():
    return setup_parser()


def test_doc(p):
    args = p.parse_args(['doc', ])

    with patch('oriole_service.api.mexe') as run:
        main(args)
        assert run.call_count == 1


def test_d(p):
    args = p.parse_args(['d', ])

    with patch('oriole_service.api.mexe') as run:
        main(args)
        assert run.call_count == 1
