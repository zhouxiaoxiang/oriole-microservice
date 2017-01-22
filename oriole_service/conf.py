import yaml
from os import path, pardir, getcwd


class Config(object):
    """ Supply configuration.

    Examples::

        from oriole_service.conf import Config
        config = Config()
        database = config["database"]
    """

    content = ""
    max_depth = 3
    file_name = "services.cfg"

    def __new__(self, *args, **kwargs):

        if not self.content:

            # Full path
            config = ""
            curdir = getcwd()
            for _ in range(self.max_depth):
                config = path.join(curdir, self.file_name)
                if path.isfile(config):
                    break
                else:
                    curdir = path.join(curdir, pardir)

            if not config:
                raise RuntimeError("Need conf file.")

            with open(config) as f:
                self.content = yaml.load(f)

        return self.content
