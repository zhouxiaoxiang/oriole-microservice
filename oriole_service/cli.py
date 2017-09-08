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

import os
import sys
import argparse
from .modules import *
from .api import setup_yaml_parser


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
    curdir = os.getcwd()
    if curdir not in sys.path:
        sys.path.insert(0, curdir)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    add_parser(subparsers, modules)
    return parser


def main():
    setup_yaml_parser()
    parser = setup_parser()
    args = parser.parse_args()
    setup_yaml_parser()
    args.main(args)
