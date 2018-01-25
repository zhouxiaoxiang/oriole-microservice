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
from subprocess import PIPE, Popen

from nameko.exceptions import RpcTimeout
from nameko.standalone.rpc import ClusterRpcProxy

from oriole.log import logger
from oriole.ops import open_shell
from oriole.vos import exe, get_config, get_first, get_loc, get_path, sleep
from oriole.yml import get_yml

__all_services = 'services:all'


def run_client(cfg, timeout):
    with ClusterRpcProxy(cfg, timeout=timeout) as s:
        ms = s.supervisor_thread
        ms.ping()
        sleep(timeout)
        services = ms.ping_result()

        if not services:
            raise ValueError('No service.')
        else:
            print("Available services:")

            no = 1
            fmt = '%5d. %-30s => %-20s'

            for k, v in services.items():
                print(fmt % (no, k, v))
                no += 1

            all = dict(s=s)
            all.update({k: s[k] for k in services.keys()})

            open_shell(all)


def remote_test(f):
    print("\n".join([
        "                                        ",
        "----------------------------------------",
        "             __  _                      ",
        "        |\/|(_  |_) _ _  o _  __|_      ",
        "        |  |__) |  | (_) |(/_(_ |_      ",
        "                        _|              ",
        "        Usage:                          ",
        "               service.method()         ",
        "----------------------------------------",
        "                                        ",
    ]))
    print("Checking all available services now...")

    try:
        run_client(get_yml(f), timeout=3)
    except FileNotFoundError:
        print("Error: you must goto correct directory.")
    except RpcTimeout:
        print("Error: can not connect to microservice.")
    except Exception as e:
        print("Error: no available services in ms now.")


def add_one_service(all, s, v):
    all.hset(__all_services, s, v)
    all.expire(__all_services, 60)


def get_all_services(all):
    services = all.hgetall(__all_services)

    if services:
        return {s.decode(): v.decode() for s, v in services.items()}


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
