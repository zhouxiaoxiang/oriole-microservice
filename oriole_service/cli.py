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
import re
import sys
import yaml
import argparse
from .modules import *
from oriole_service import api

ENV_VAR_MATCHER = re.compile(r"""
        \$\{       # match characters `${` literally
        ([^}:\s]+) # 1st group: matches any character except `}` or `:`
        :?         # matches the literal `:` character zero or one times
        ([^}]+)?   # 2nd group: matches any character except `}`
        \}         # match character `}` literally
    """, re.VERBOSE)

IMPLICIT_ENV_VAR_MATCHER = re.compile(r"""
        .*          # matches any number of any characters
        \$\{.*\}    # matches any number of any characters
                    # between `${` and `}` literally
        .*          # matches any number of any characters
    """, re.VERBOSE)


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


def _replace_env_var(match):
    env_var, default = match.groups()
    return os.environ.get(env_var, default)


def _env_var_constructor(loader, node):
    value = loader.construct_scalar(node)
    return ENV_VAR_MATCHER.sub(_replace_env_var, value)


def setup_yaml_parser():
    yaml.add_constructor('!env_var', _env_var_constructor)
    yaml.add_implicit_resolver('!env_var', IMPLICIT_ENV_VAR_MATCHER)


def main():
    parser = setup_parser()
    args = parser.parse_args()
    setup_yaml_parser()
    args.main(args)
