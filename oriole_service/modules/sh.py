""" Test remote services. """

from __future__ import print_function

import code
import yaml
from nameko.standalone.rpc import ClusterRpcProxy


def main(args):

    usage = "Usage: services.log_service.ping()"

    with open(args.config) as f:
        config = yaml.load(f)

    with ClusterRpcProxy(config) as services:
        local = {}
        local.update({"services": services})
        code.interact(usage, None, local)


def init_parser(parser):
    parser.add_argument(
        '--config', default='services.cfg', help='services.cfg')
    return parser
