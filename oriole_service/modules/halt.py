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
#    )                Halt services              (
#    '-------------------------------------------'
#

from oriole_service import api


def main(args):
    api.halt(args.service)


def init_parser(parser):
    parser.add_argument('service', metavar='service', help='Service')
