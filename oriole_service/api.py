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

from nameko.standalone.rpc import ClusterRpcProxy

from oriole.log import logger
from oriole.ops import open_shell
from oriole.vos import exe, get_config, get_first, get_loc, get_path
from oriole.yml import get_yml


def remote_test(f):
    with ClusterRpcProxy(get_yml(f), timeout=3) as s:
        open_shell(s)


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
