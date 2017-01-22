import sys
from os import path, pardir, getcwd
from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler
from oriole_service.conf import Config
from oriole_service.log import logger

topdir = path.join(getcwd(), pardir, pardir)
sys.path.insert(0, topdir)
from dao import *


class App(object):
    """ App base.

    Examples::

        from oriole_service.app import App
        app = App()
    """

    # mysql
    db = ""

    # redis
    rs = ""

    # config
    cf = ""

    def init(self):
        self._log = logger()
        self._log.info('Create app...')

        data = Db()
        self.db = data.get_db()
        self.rs = data.get_rs()
        self.cf = Config()

    def obj2dict(self, obj):
        return dict((key, obj.__dict__[key])\
               for key in obj.__dict__ \
               if not key.startswith("_"))
