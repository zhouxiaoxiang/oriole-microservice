""" Run services. """

from __future__ import print_function

import sys
import errno
import shutil
from os import path
from logging import getLogger

_log = getLogger(__name__)


def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            _log.error('Error: %s' % e)


def main(args):
    if path.exists(args.name):
        _log.warning('Service already exists')
        return
    else:
        _log.info('Create service files.')
        templates = path.join(path.dirname(__file__), 
                              path.pardir, "templates")
        copy(templates, args.name)


def init_parser(parser):
    parser.add_argument('name', metavar='name', 
                        help='Service name')

    return parser
