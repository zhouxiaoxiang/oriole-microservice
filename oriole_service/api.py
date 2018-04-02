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

from os import chdir
from os import path
from subprocess import PIPE, Popen

from nameko.exceptions import RpcTimeout
from nameko.standalone.rpc import ClusterRpcProxy as cluster

from oriole.db import get_redis
from oriole.log import logger
from oriole.ops import open_shell
from oriole.vos import exe, mexe, get_config, get_first, get_loc, get_path, sleep, switch_lang
from oriole.yml import get_yml

_SERVICE_CK = '>>> Check online services.......'
_SERVICE_NO = '>>> No services, Try ls() later.'
_SERVICE_OK = '>>> Show online micro services:'
_SERVICE_CF = '>>> Error: correct directory ?'
_SERVICE_TM = '>>> Error: connection fails.'
_SERVICE_PY = '>>> Error: wrong service name.'
_SERVICE_TS = '>>> Error: wrong test name.'
_SERVICE_PK = '>>> Error: can not kill %s.'
_SERVICE_CS = '%-30s => %-20s'
_SERVICE_EX = 'nameko run %s --config %s'


def _ls(s, rs, sh):
    print(_SERVICE_CK)
    sleep(1)
    services = get_all_services(rs)

    if not services:
        print(_SERVICE_NO)
    else:
        print(_SERVICE_OK)
        mexe(lambda n: print(
            _SERVICE_CS % (n, services.get(n))),
            sorted(services.keys()))
        sh.update({k: s[k] for k in services.keys()})


def remote_test(f, time=5):
    try:
        cfg = get_yml(f)
        with cluster(cfg, timeout=time) as s:
            sh = {}
            rs = get_redis(cfg.get('datasets'))
            sh.update(dict(ls=lambda: _ls(s, rs, sh)))
            _ls(s, rs, sh)
            open_shell(sh)

    except FileNotFoundError:
        print(_SERVICE_CF)
    except RpcTimeout:
        print(_SERVICE_TM)


def add_service(all, s, v, n, expire=30):
    all.sadd('services', s)
    all.expire('services', expire)
    all.set('services:' + s, '%s|%s' % (n, v), expire)


def get_all_services(all):
    services = all.smembers('services')
    if services:
        services = {s.decode() for s in services}
        return get_all_available_services(all, services)


def get_all_available_services(all, services_all):
    services = {}

    for s in services_all:
        v = all.get('services:' + s)
        if v:
            services[s] = v.decode()

    return services


def run(service):
    try:
        chdir(get_path("%s.py" % service, "services"))
    except:
        raise RuntimeError(_SERVICE_PY)
    else:
        exe(_SERVICE_EX % (service, get_loc()))


def test(service):
    try:
        chdir(get_path("test_%s.py" % service, "tests"))
    except:
        raise RuntimeError(_SERVICE_TS)
    else:
        exe("py.test")


def get_logger():
    cf = get_config()
    level = cf.get("log_level", "DEBUG")
    name = cf.get("log_name", "")

    return logger(name, level)


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
        raise RuntimeError(_SERVICE_PK % service)


def change_lang(lang='zh'):
    loc = 'i18n'
    i18n_loc = get_loc(loc, False)
    if i18n_loc:
        loc = path.join(i18n_loc, loc)
        switch_lang(lang, loc)
