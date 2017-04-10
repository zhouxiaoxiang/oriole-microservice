""" Goto remote host  """

from __future__ import print_function
import os
import subprocess


def main(args):
    for choice in ['nc', 'telnet']:
        if os.system('which %s' % choice) == 0:
            prog = choice
            break
    else:
        raise RuntimeError('Have no goto tool.')

    target = args.target
    if ':' in target:
        host, port = target.split(':', 1)
    else:
        host, port = 'localhost', target

    cmd = "%s %s %s" % (prog, str(host), str(port))

    try:
        if subprocess.run(cmd, shell=True) != 0:
            raise RuntimeError('Unreachable')
    except (EOFError, KeyboardInterrupt):
        subprocess.run('reset', shell=True)


def init_parser(parser):
    parser.add_argument(
        'target', metavar='[host:]port', help="Target to connect to")
    parser.set_defaults(feature=True)
    return parser
