""" Run services. """

from oriole_service import api
from os.path import *


def main(args):
    proj = join(dirname(__file__), pardir, "proj")
    api.copy(proj, args.name)


def init_parser(parser):
    parser.add_argument('name', metavar='name', help='Service name')
