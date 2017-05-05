""" Test services. """

from oriole_service import api


def main(args):
    api.test(args.services)


def init_parser(parser):
    parser.add_argument(
        'services', nargs='*', metavar='services', help='Services')
