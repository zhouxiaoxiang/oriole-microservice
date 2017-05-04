""" Oriole-APP """

import sys
import copy
from os import path, pardir, getcwd
from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler
from oriole_service.api import Config
from oriole_service.db import *
from datetime import datetime
from decimal import Decimal

topdir = path.join(getcwd(), pardir, pardir)
sys.path.insert(0, topdir)
from dao import *


class App(object):

    db = ""
    rs = ""
    cf = ""
    name = "supervisor_thread"

    def init(self):
        data = Db(Base)
        self.db = data.get_db()
        self.rs = data.get_rs()
        self.cf = Config()

    @rpc
    def ping(self):
        return True

    #
    # These methods are used in services.
    # NOT use in oriole-service anytime.
    #

    def _(self, item):
        """ Get item from params """

        if isinstance(item, dict):
            self._params = copy.deepcopy(item)
            return self._params

        try:
            return self._params.get(item)
        except:
            return RuntimeError("Use self._(params) first.")

    def _o(self, obj):
        """ Translate object to json.

        Dict in python is not json, so don't be confused.
        When return object from rpc, should always use _o.
        """

        if isinstance(obj, (list, set, tuple)):
            return self._ol(obj)
        elif isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, dict):
            return self._od(obj)
        elif obj == None or isinstance(obj, (int, str, bool, float)):
            return obj
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return self._oo(obj)

    def _oo(self, obj):
        """ Don't use it! """

        result = {}
        for key in dir(obj):
            if key != "metadata" and key[0] != "_":
                value = getattr(obj, key)
                if not callable(value):
                    result[key] = self._o(value)
        return result

    def _ol(self, obj):
        """ Don't use it! """

        return [self._o(item) for item in obj]

    def _od(self, obj):
        """ Don't use it! """

        return {item: self._o(obj[item]) for item in obj}

    def obj2dict(self, obj):
        """ Don't use it! """

        return self._oo(obj)
