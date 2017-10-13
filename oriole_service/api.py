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
import re
import yaml
import logging
import tempfile
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


def _replace_env_var(match):
    env_var, default = match.groups()
    return os.environ.get(env_var, default)


def _env_var_constructor(loader, node):
    var = re.compile(r"\$\{([^}:\s]+):?([^}]+)?\}", re.VERBOSE)
    value = loader.construct_scalar(node)
    return var.sub(_replace_env_var, value)


def setup_yaml_parser():
    var = re.compile(r".*\$\{.*\}.*", re.VERBOSE)
    yaml.add_constructor('!env_var', _env_var_constructor)
    yaml.add_implicit_resolver('!env_var', var)


def get_config(f="services.cfg"):
    return get_yml(get_file(f))


def get_yml(f):
    setup_yaml_parser()
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


def build(service):
    fmt = "docker build -t {}_service -f {} ."
    tmp = tempfile.NamedTemporaryFile(dir=".")
    try:
        tmp.write(b"FROM zhouxiaoxiang/service\n")
        tmp.write(b"COPY . /service\n")
        tmp.write(b"WORKDIR /service\n")
        tmp.write(b"RUN make\n")
        tmp.write("CMD o r {}\n".format(service).encode())
        tmp.seek(0)
        exe(fmt.format(service, tmp.name))
    finally:
        tmp.close()


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
    with ClusterRpcProxy(get_yml(f)) as s:
        try:
            from IPython import embed
            embed()
        except:
            scope = dict(s=s)
            import code
            code.interact(None, None, scope)


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
