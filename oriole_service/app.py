import sys
from os import path, pardir, getcwd
from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler
from oriole_service.conf import Config
from oriole_service.log import logger
from oriole_service.db import *
from datetime import datetime

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

        data = Db(Base)
        self.db = data.get_db()
        self.rs = data.get_rs()
        self.cf = Config()

    def obj2dict(self, obj):
        result = {}
        for key in dir(obj):
            if not key.startswith("_"):
                value = getattr(obj, key)
                if not callable(value):
                    result[key] = self._obj2json(value)
        return result


    def _list2json(self, obj):
        result = []
        for item in obj:
            result.append(self._obj2json(item))
        return result


    def _dict2json(self, obj):
        result = {}
        for item in obj:
            result[item] = self._obj2json(obj[item])
        return result


    def _obj2json(self, obj):
        if isinstance(obj, (list, set, tuple)):
            return self._list2json(obj)
        elif isinstance(obj, dict):
            return self._dict2json(obj)
        elif obj == None or isinstance(obj, (int, str, bool, float)):
            return obj
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return self.obj2dict(obj)
