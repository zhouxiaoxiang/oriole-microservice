from __future__ import print_function
import argparse
import os
import sys
import re
import yaml
from . import doc, test, run, go, goto

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


def setup_parser():
    curdir = os.getcwd()
    if curdir not in sys.path:
        sys.path.insert(0, curdir)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    for module in [doc, test, run, go, goto]:
        name = module.__name__.split('.')[-1]
        module_parser = subparsers.add_parser(name, description=module.__doc__)
        module.init_parser(module_parser)
        module_parser.set_defaults(main=module.main)
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
