""" Test services. """

from __future__ import print_function

import sys
import subprocess
from os import path, walk
from logging import getLogger

_log = getLogger(__name__)


def run(test=''):
    loc = "tests"
    cmd = "py.test -v"

    if not test:
        subprocess.run(cmd, shell=True)
        return

    for fpath, _, fs in walk(loc):
        if ("test_%s" % test + ".py") in fs:
            fmt = "cd %s && %s" % (fpath, cmd)
            subprocess.run(fmt, shell=True)
            break

def main(args):
    _log.debug("Test %s", args.service)
    if not args.service:
        run()
    else:
        for test in args.service:
            run(test)

def init_parser(parser):
    parser.add_argument(
        'service', nargs='*', 
        metavar='service',
        help='Service to test')

    return parser
