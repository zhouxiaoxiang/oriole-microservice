from mock import patch
from oriole_service.cli import setup_parser
from oriole_service.modules.run import main, run


def test_main():
    parser = setup_parser()
    args = parser.parse_args([
        'run',
        'log',
    ])

    with patch('oriole_service.modules.run.run') as run:
        main(args)
        assert run.call_count == 1
        assert run.call_args[0][0] == 'log'
