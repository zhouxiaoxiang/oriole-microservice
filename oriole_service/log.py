""" Oriole-LOG """

import mogo
from oriole_service.api import Config, logger


class Log:
    def __init__(self, module=""):
        conf = Config()['log'][module]
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
