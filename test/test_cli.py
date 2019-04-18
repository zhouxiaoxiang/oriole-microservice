import sys

from mock import patch
from pytest import *

from oriole_service.cli import main


@fixture
def eric():
    sys.argv = ['o', 'r', 'eric']


def test_run(eric):
    with patch('oriole_service.api.run') as run:
        main()
        assert run.call_count == 1
        assert run.call_args[0][0] == 'eric'
