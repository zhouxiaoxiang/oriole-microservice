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
#     )                Oriole-CLI               (
#    (                  Eric.Zhou                )
#     )              Build services             (
#    '-------------------------------------------'
#

from oriole.ops import build


def main(args):
    build(args.service)


def init_parser(parser):
    parser.add_argument('service', metavar='service', help='Service')
