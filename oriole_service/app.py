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
#     )                Oriole-APP               (
#    (                  Eric.Zhou                )
#    '-------------------------------------------'
#

import copy
from datetime import date, datetime
from decimal import Decimal

from nameko.events import EventDispatcher, event_handler
from nameko.rpc import RpcProxy, rpc, Rpc
from nameko.timer import timer

from dao import *
from oriole.vos import cwd, get_config, service_name
from oriole_service import *
from oriole_service.api import add_service, get_logger, change_lang
from oriole_service.db import *

change_lang('en')
SUPER_THREAD = 'super_thread'


class App:
    """ Connect database

    As usual, supply mysql and redis.
    """

    db = Db(Base)
    rs = Rs()
    log = get_logger()
    ver = "1.0.0"
    name = SUPER_THREAD

    def init(self):
        ''' Noop '''

    @rpc
    def ping(self, name=name):
        return True

    @rpc
    def version(self):
        return self.ver

    @timer(10)
    def update_service(self):
        if self.name != SUPER_THREAD:
            add_service(self.rs, self.name, self.ver)

    #
    # These methods are used in services.
    # NOT use in oriole code anytime.
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
