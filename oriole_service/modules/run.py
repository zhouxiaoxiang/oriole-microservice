""" Run services. """

from oriole_service import api


def main(args):
    api.run(args.service)


def init_parser(parser):
    parser.add_argument('service', metavar='service', help='Service to run')
