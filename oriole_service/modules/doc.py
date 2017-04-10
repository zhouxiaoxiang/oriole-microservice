""" Create documents of services. """

from __future__ import print_function

import sys
import subprocess
from os import path, walk
from logging import getLogger

_log = getLogger(__name__)


def run(fmt):
    _log.debug('Create documents...')
    subprocess.run("sphinx-apidoc -f -o \
            docs services", shell=True)
    subprocess.run("sphinx-build -b %s docs \
            docs/build/html" % fmt, shell=True)

def main(args):
    run(args.format)

def init_parser(parser):
    parser.add_argument(
        '--format', default='html', 
        help='Format of files')

    return parser
