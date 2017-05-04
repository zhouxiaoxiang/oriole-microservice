""" Oriole-API """

import os
import yaml
import code
import shutil
import subprocess
from os import path, walk, pardir, getcwd
from nameko.standalone.rpc import ClusterRpcProxy


def Config(name="services.cfg"):
    f = getf(name)
    if not f:
        raise RuntimeError('Need {}'.format(name))
    return get_yml(f)


def get_yml(f):
    with open(f) as filename:
        return yaml.load(filename)


def getf(f):
    max_depth = 3
    loc = getcwd()

    for _ in range(max_depth):
        config = path.join(loc, f)
        if path.isfile(config):
            return config
        else:
            loc = path.join(loc, pardir)
    return ""


def exe(s):
    subprocess.run(s, shell=True)


def mexec(f, s):
    return [i for i in map(f, s)]


def cwd():
    return os.getcwd()


def run(service):
    config = path.join(cwd(), "services.cfg")
    for fpath, _, fs in walk("services"):
        if (service + ".py") in fs:
            fmt = "cd {} && nameko run {} --config {}"
            cmd = fmt.format(fpath, service, config)
            exe(cmd)
            break


def remote_test(args):
    usage = "Usage: services.log_service.ping()"

    config = get_yml(args.config)
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
