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
from nameko.standalone.rpc import ClusterRpcProxy

from oriole.db import get_redis
from oriole.log import logger
from oriole.ops import open_shell
from oriole.vos import exe, get_config, get_first, get_loc, get_path, sleep, switch_lang
from oriole.yml import get_yml


def _ls(s, rs, retry=False):
    print("Checking all available services now...")
    sleep(1)
    services = get_all_services(get_redis(rs))

    if not services:
        print('Error: no available services in ms now.')
    else:
        print("Available services:")
        service_no = 1
        fmt = '%5d. %-30s => %-20s'

        for k, v in services.items():
            print(fmt % (service_no, k, v))
            service_no += 1

        all = dict(s=s, ls=lambda: _ls(s, rs, True))
        all.update({k: s[k] for k in services.keys()})

        if not retry:
            return all


def remote_test(f):
    print("\n".join([
        "                                        ",
        "----------------------------------------",
        "                                        ",
        "            __  _                       ",
        "       |\/|(_  |_) _ _  o _  __|_       ",
        "       |  |__) |  | (_) |(/_(_ |_       ",
        "                       _|               ",
        "                                        ",
        "----------------------------------------",
        "                                        ",
    ]))

    try:
        cfg = get_yml(f)
        with ClusterRpcProxy(cfg, timeout=5) as s:
            all = _ls(s, cfg.get('datasets'))

            if all:
                open_shell(all)

    except FileNotFoundError:
        print("Error: you must goto correct directory.")
    except RpcTimeout:
        print("Error: can not connect to microservice.")


def add_one_service(all, s, v):
    expire = 30
    all.sadd('services', s)
    all.expire('services', expire)
    all.set('services:' + s, v, expire)


def get_all_services(all):
    services_all = all.smembers('services')

    if services_all:
        services_all = {s.decode() for s in services_all}

        return get_all_available_services(all, services_all)


def get_all_available_services(all, services_all):
    available_services = {}

    for s in services_all:
        v = all.get('services:' + s)

        if v:
            available_services[s] = v.decode()

    return available_services


def run(service):
    chdir(get_path("%s.py" % service, "services"))
    exe("nameko run %s --config %s" % (
        service, get_loc())
        )


def test(service):
    chdir(get_path("test_%s.py" % service, "tests"))
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
        raise RuntimeError("Error: cannot kill %s." % service)


def change_lang(lang='zh'):
    loc = 'i18n'
    i18n_loc = get_loc(loc, False)
    if i18n_loc:
        loc = path.join(i18n_loc, loc)
        switch_lang(lang, loc)
