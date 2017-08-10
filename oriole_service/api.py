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
#     )                Oriole-API               (
#    (                  Eric.Zhou               )
#    '-------------------------------------------'
#

import os
import yaml
import code
import shutil
import logging
import tempfile
import contextlib
from subprocess import run as sr
from subprocess import Popen, PIPE
from os import path, walk, pardir, getcwd
from nameko.standalone.rpc import ClusterRpcProxy
from logging import DEBUG, INFO, WARNING, ERROR
from logging import StreamHandler, Formatter, getLogger, FileHandler

exe = lambda s: sr(s, shell=True)
mexe = lambda f, s: tuple(map(f, s))
cwd = lambda: getcwd()
test_cmd = "py.test -v --html=report.html"
get_first = lambda s: s.strip().split()[0]


def get_config(f="services.cfg"):
    return get_yml(get_file(f))


def get_yml(f):
    with open(f) as filename:
        return yaml.load(filename)


def get_file(f):
    loc = cwd()
    for _ in range(3):
        config = path.join(loc, f)
        if path.isfile(config):
            return config
        loc = path.join(loc, pardir)


def get_path(f, loc):
    for fpath, _, fs in walk(loc):
        if f in fs:
            return fpath


def run(service):
    fmt = "cd %s && nameko run %s --config %s"
    config = path.join(cwd(), "services.cfg")
    fpath = get_path("%s.py" % service, "services")
    if fpath:
        exe(fmt % (fpath, service, config))


def halt(service):
    comm_ps = ["ps", "ax"]
    comm_nameko = ["grep", "nameko run %s" % service]
    comm_python = ["grep", "python"]

    try:
        p_all = Popen(comm_ps, stdout=PIPE)
        p_rpc = Popen(comm_nameko, stdin=p_all.stdout, stdout=PIPE)
        p_result = Popen(comm_python, stdin=p_rpc.stdout, stdout=PIPE)
        p_all.stdout.close()
        p_rpc.stdout.close()

        proc = p_result.communicate()[0]
        if proc:
            pid = int(get_first(proc))
            exe("kill %s" % pid)
    except:
        raise RuntimeError("Error: cannot kill %s." % service)


def remote_test(f):
    usage = 'Usage: s.log_service.ping()'
    config = get_yml(f)
    with ClusterRpcProxy(config) as s:
        code.interact(usage, None, {"s": s})


def mtest(test):
    fmt = "cd %s && %s"
    fpath = get_path("test_%s.py" % test, "tests")
    if fpath:
        exe(fmt % (fpath, test_cmd))


def test(tests):
    if not tests:
        exe(test_cmd)
    else:
        mexe(mtest, tests)


def Config(name="services.cfg"):
    """ Obsoleted """
    return get_config(name)


def logger(level='DEBUG', name=""):
    fmt = '[%(module)s] %(asctime)s %(levelname)-7.7s %(message)s'
    dfmt = '%Y-%m-%d %H:%M:%S'
    level = getattr(logging, level, DEBUG)

    logger = getLogger('services')
    logger.setLevel(level)
    fmter = Formatter(fmt, dfmt)
    del logger.handlers[:]

    if name:
        fh = FileHandler(name)
        fh.setLevel(level)
        fh.setFormatter(fmter)
        logger.addHandler(fh)

    ch = StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmter)
    logger.addHandler(ch)
    logger.propagate = False

    return logger


def get_logger():
    cf = get_config()
    level = cf.get("log_level", "DEBUG")
    name = cf.get("log_name", "")
    return logger(level, name)


@contextlib.contextmanager
def get_cfg(f):
    try:
        loc = tempfile.mkdtemp()
        name = "%s/%s" % (loc, f)
        shutil.copy(f, loc)
        yield name
        shutil.copy(name, f)
    finally:
        os.remove(name)
        os.rmdir(loc)


def check(f):
    try:
        get_yml(f)
        return True
    except Exception as e:
        input(str(e))
        return False


def conf(name):
    with get_cfg(name) as f:
        ed = os.environ.get('EDITOR', 'vi')
        while True:
            exe('%s "%s"' % (ed, f))
            if check(f): break
