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
#     )                Oriole-LOG               (
#    (                  Eric.Zhou               )
#    '-------------------------------------------'
#

import mogo
from oriole_service.api import get_config
from oriole_service.api import get_logger as logger


class Log:
    def __init__(self, module=""):
        conf = get_config()['log'][module]
        self.host = conf['host']
        self.db = conf['db']
        self.tb = conf['tb']

        try:
            self.conn = mogo.connect(self.db, self.host)
            self.log = self.conn[self.db][self.tb]
        except:
            raise RuntimeError("Error: Mongo is down.")

    def get(self):
        return self.log
