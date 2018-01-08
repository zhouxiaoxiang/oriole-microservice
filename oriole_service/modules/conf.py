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
#    )               Test services              (
#    '-------------------------------------------'
#

from oriole_service.cf import write


def main(args):
    write(args.directory, args.outfile, args.infile)


def init_parser(parser):
    parser.add_argument('directory', metavar='directory', nargs='?',
                        default='/ms/test/', help="server's directory")

    parser.add_argument('outfile', metavar='outfile', nargs='?',
                        default='services.cfg', help="services.cfg")

    parser.add_argument('infile', metavar='infile', nargs='?',
                        default='services.in', help="services.in")
