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

from jinja2.ext import Extension


class CfExtension(Extension):
    '''Restore configuration.'''

    def __init__(self, env):
        super().__init__(env)

        def read(k):
            from oriole_service.cf import read

            return read(k)

        env.globals.update({'_': read})
