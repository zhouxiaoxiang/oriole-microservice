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
#     )                Oriole-CLI               (
#    (                  Eric.Zhou               )
#    )            Test remote services          (
#    '-------------------------------------------'
#

from oriole_service import api


def main(args):
    api.remote_test(args.config, args.server)


def init_parser(parser):
    parser.add_argument('--config', default='services.cfg', help='config')
    parser.add_argument('--server', default='')
