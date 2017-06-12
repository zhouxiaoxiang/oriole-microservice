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
#    )        Create documents of services      (
#    '-------------------------------------------'
#

from oriole_service import api


def main(args):
    cmds = ("sphinx-apidoc -f -o docs services",
            "sphinx-build -b %s docs docs/build/html" % args.format)
    api.mexe(api.exe, cmds)


def init_parser(parser):
    parser.add_argument('--format', default='html', help='Format')
