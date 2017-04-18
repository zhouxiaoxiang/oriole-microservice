""" Test services. """

from oriole_service import api


def main(args):
    if not args.service:
        api.test()
    else:
        api.mexec(api.test, args.service)


def init_parser(parser):
    parser.add_argument(
        'service', nargs='*', metavar='service', help='Service to test')
