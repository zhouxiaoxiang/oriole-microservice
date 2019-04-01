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
#     )                 Oriole-CF               (
#    (                  Eric.Zhou                )
#    '-------------------------------------------'
#

from oriole.cf import MsConfig
from oriole.vos import get_config


# Create configuration for every microservice, not all.
try:
    ms_hosts = get_config('oc.cfg').get('etcds', 'localhost')
except Exception:
    ms_hosts = 'localhost'

_cf = MsConfig('oriole_service.ext.CfExtension', ms_hosts=ms_hosts)

# Supply r/w for configuration files.
write, read = _cf.write, _cf.read
