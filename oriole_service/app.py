""" Oriole-APP """

import sys
import copy
from os import path, pardir
from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler
from oriole_service.api import Config, cwd
from oriole_service.db import *
from datetime import datetime, date
from decimal import Decimal

topdir = path.join(cwd(), pardir, pardir)
sys.path.insert(0, topdir)
from dao import *


class App(object):

    db = ""
    rs = ""
    cf = Config()
    name = "supervisor_thread"

    def init(self):
        self.db = Db(Base).get_db()
        self.rs = Db(Base).get_rs()

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
            raise RuntimeError("Use self._(params) first.")

    def _o(self, obj):
        """ Translate object to json.

        Dict in python is not json, so don't be confused.
        When return object from rpc, should always use _o.
        """

        if obj == None:
            return obj
        elif isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, (list, set, tuple)):
            return self._ol(obj)
        elif isinstance(obj, dict):
            return self._od(obj)
        elif isinstance(obj, (int, str, bool, float)):
            return obj
        else:
            return self._oo(obj)

    def _oo(self, obj):
        """ Don't use it! """

        result = {}
        try:
            for key in dir(obj):
                if key != "metadata" and key[0] != "_":
                    value = getattr(obj, key)
                    if not callable(value):
                        result[key] = self._o(value)
        except:
            raise RuntimeError("NOT support %s" % (type(obj)))

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
