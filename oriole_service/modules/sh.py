""" Test remote services. """

from oriole_service import api


def main(args):
    api.remote_test(args)


def init_parser(parser):
    parser.add_argument(
        '--config', default='services.cfg', help='services.cfg')
