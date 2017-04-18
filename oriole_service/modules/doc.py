""" Create documents of services. """

from oriole_service import api


def run(fmt):
    cmds = ("sphinx-apidoc -f -o docs services",
            "sphinx-build -b %s docs docs/build/html" % fmt)
    api.mexec(api.exe, cmds)


def main(args):
    run(args.format)


def init_parser(parser):
    parser.add_argument('--format', default='html', help='Format of docs')
