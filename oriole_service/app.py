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
#     )                Oriole-APP               (
#    (                  Eric.Zhou               )
#    '-------------------------------------------'
#

import sys
import copy
from os import path, pardir
from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler
from oriole_service.api import get_config, cwd, get_logger
from oriole_service.db import *
from datetime import datetime, date
from decimal import Decimal

topdir = path.join(cwd(), pardir, pardir)
sys.path.insert(0, topdir)
from dao import *


class App:
    """ Connect database

    As usual, supply mysql and redis.
    """

    db = Db(Base)
    rs = Rs()
    log = get_logger()
    ver = "1.0.0"
    name = "supervisor_thread"

    def init(self):
        ''' Noop '''

    @rpc
    def ping(self):
        return True

    @rpc
    def version(self):
        return self.ver

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
            raise RuntimeError("Error: Use self._(params) first.")

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
            raise RuntimeError("Error: %s, only support json" % (type(obj)))

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
