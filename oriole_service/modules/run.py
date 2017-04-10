""" Run services. """

from __future__ import print_function

import sys
import subprocess
from os import path, walk
from logging import getLogger

_log = getLogger(__name__)


def run(service):
    loc = "services"
    curdir = path.abspath(path.curdir)
    config = path.join(curdir, "services.cfg")

    for fpath, _, fs in walk(loc):
        if (service + ".py") in fs:
            fmt = "cd %s && nameko run %s --config %s"
            cmd = fmt % (fpath, service, config)
            subprocess.run(cmd, shell=True)
            break

def main(args):
    _log.debug('Run %s', args.service)
    run(args.service)

def init_parser(parser):
    parser.add_argument(
        'service', 
        metavar='service',
        help='Service to run')

    return parser
