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
#     )                Oriole-LOG               (
#    (                  Eric.Zhou                )
#    '-------------------------------------------'
#

from nameko.extensions import DependencyProvider

from oriole.db import get_mongo
from oriole.vos import get_config


class Log(DependencyProvider):
    def __init__(self, module=''):
        conf = get_config()['log'][module]
        self.host = conf['host']
        self.db = conf['db']
        self.tb = conf['tb']

    def setup(self):
        try:
            self.conn = get_mongo(self.db, self.host)
            self.log = self.conn[self.db][self.tb]
        except Exception:
            raise RuntimeError("Error: Mongo is down.")

    def get_dependency(self, worker_ctx):
        return self.log
