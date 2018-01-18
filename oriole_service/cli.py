#
#                __   _,--="=--,_   __
#               /  \."    .-.    "./  \
#              /  ,/  _   : :   _  \/` \
#              \  `| /o\  :_:  /o\ |\__/
#               `-'| :="~` _ `~"=: |
#                  \`     (_)     `/
#           .-"-.   \      |      /   .-"-.
#    .-----{     }--|  /,.-'-.,\  |--{     }-----.
#     )    (_)_)_)  \_/`~-===-~`\_/  (_(_(_)    (
#    (                                          )
#     )                Oriole-CLI               (
#    (                  Eric.Zhou               )
#    '-------------------------------------------'
#

import argparse

from oriole_service.api import setup_yaml_parser
from oriole_service.modules import *


def _add_parser(parser, module, name):
    module_parser = parser.add_parser(name, description=module.__doc__)
    module.init_parser(module_parser)
    module_parser.set_defaults(main=module.main)


def add_parser(parser, modules):
    for module in modules:
        name = module.__name__.split('.')[-1]
        _add_parser(parser, module, name)
        _add_parser(parser, module, name[0])


def setup_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    add_parser(subparsers, modules)

    return parser


def main():
    setup_yaml_parser()
    parser = setup_parser()
    args = parser.parse_args()
    args.main(args)
