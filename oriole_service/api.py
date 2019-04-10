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
#    (                                           )
#     )                Oriole-API               (
#    (                  Eric.Zhou                )
#    '-------------------------------------------'
#

from os import path
from subprocess import PIPE, Popen

from nameko.exceptions import RpcTimeout
from nameko.standalone.rpc import ClusterRpcProxy as cluster

from oriole.log import logger
from oriole.ops import open_shell
from oriole.vos import exe, get_config, get_first, get_loc, get_path, mexe, switch_lang
from oriole.yml import get_yml

_SERVICE_CK = '>>> Check online services...'
_SERVICE_NO = '>>> Try ls() to check again.'
_SERVICE_OK = '>>> Online services:'
_SERVICE_CF = '>>> Error: correct directory ?'
_SERVICE_TM = '>>> Error: connection fails.'
_SERVICE_PK = '>>> Error: can not kill %s.'
_SERVICE_CS = '%-30s => %-20s'
_SERVICE_EX = 'nameko run %s --config %s'
_SERVICE_MQ = 'pyamqp://%s'
_SERVICE_FT = '[%(module)s] %(asctime)s %(levelname)-7.7s %(message)s'


def _ls(s, sh):
    print(_SERVICE_CK)
    try:
        services = s.super_thread.ms_services()
    except Exception:
        services = {}

    if not services:
        print(_SERVICE_NO)
    else:
        print(_SERVICE_OK)
        mexe(lambda n: print(_SERVICE_CS % (n, services.get(n))),
             sorted(services.keys()))
        sh.update({k: s[k] for k in services.keys()})


def remote_test(fil, server, time=5):
    try:
        cfg = {}
        if not server:
            cfg = get_yml(fil)
        else:
            cfg['AMQP_URI'] = _SERVICE_MQ % server

        with cluster(cfg, timeout=time) as s:
            sh = {}
            sh.update(dict(ls=lambda: _ls(s, sh)))
            _ls(s, sh)
            open_shell(sh)
    except FileNotFoundError:
        print(_SERVICE_CF)
    except RpcTimeout:
        print(_SERVICE_TM)


def run(service):
    exe(_SERVICE_EX % (service, get_loc()),
        get_path("%s.py" % service, "services"))


def test(service):
    return exe("py.test", get_path("test_%s.py" % service, "tests")).returncode


def get_logger():
    cf = get_config()
    fmt = cf.get('fmt', _SERVICE_FT)
    dfmt = cf.get('dfmt', '%Y-%m-%d %H:%M:%S')
    level = cf.get("log_level", "DEBUG")

    return logger(level, fmt, dfmt)


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
    except Exception:
        raise RuntimeError(_SERVICE_PK % service)


def change_lang(lang='zh'):
    loc = 'i18n'
    i18n_loc = get_loc(loc, False)
    if i18n_loc:
        loc = path.join(i18n_loc, loc)
        switch_lang(lang, loc)
