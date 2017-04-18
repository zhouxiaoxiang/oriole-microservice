""" API. """

import os
import yaml
import code
import shutil
import subprocess
from os import path, walk
from nameko.standalone.rpc import ClusterRpcProxy


def exe(s: str):
    subprocess.run(s, shell=True)


def mexec(f, s):
    return [ i for i in map(f, s) ]


def cwd() -> str:
    return os.getcwd()


def copy(src: str, dest: str):
    shutil.copytree(src, dest)


def run(service: str):
    config = path.join(cwd(), "services.cfg")
    for fpath, _, fs in walk("services"):
        if (service + ".py") in fs:
            fmt = "cd {} && nameko run {} --config {}"
            cmd = fmt.format(fpath, service, config)
            exe(cmd)
            break


def remote_test(args):
    usage = "Usage: services.log_service.ping()"

    with open(args.config) as f:
        config = yaml.load(f)

    with ClusterRpcProxy(config) as s:
        local = {}
        local.update({"services": s})
        code.interact(usage, None, local)


def test(test=''):
    cmd = "py.test -v"

    if not test:
        exe(cmd)
        return

    for fpath, _, fs in walk("tests"):
        if ("test_%s" % test + ".py") in fs:
            exe("cd {} && {}".format(fpath, cmd))
            break
