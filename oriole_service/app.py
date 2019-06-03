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
from nameko.rpc import Rpc, RpcProxy, rpc
from nameko.timer import timer
from nameko_tracer import Tracer

from dao import *
from oriole.vos import cwd, get_config, service_name, _, _o, _oo, _ol, _od, obj2dict
from oriole_service import *
from oriole_service.api import change_lang, get_logger
from oriole_service.db import *

change_lang('en')
SUPER_THREAD = 'super_thread'


class App:
    """ Connect database """

    ver = "0.0.1"
    db = Db(Base)
    rs = Rs()
    log = get_logger()
    name = SUPER_THREAD
    tracer = Tracer()

    def init(self):
        ''' Only for legacy '''

    @rpc
    def ms_services(self):
        if self.name == SUPER_THREAD:
            return get_all_services(self.rs)

    @rpc
    def ms_config(self):
        if self.name != SUPER_THREAD:
            return self.rs.current_ms_config

    @rpc
    def ms_ping(self):
        if self.name != SUPER_THREAD:
            return True

    @rpc
    def ms_version(self):
        if self.name != SUPER_THREAD:
            return self.ver

    @timer(10)
    def ms_update_service(self):
        if self.name != SUPER_THREAD:
            add_service(self.rs, self.name, self.ver)

    # Only used in services.
    _ = _
    _o = _o
    _oo = _oo
    _ol = _ol
    _od = _od
    obj2dict = obj2dict
