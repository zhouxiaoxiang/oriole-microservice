import mogo
from logging import getLogger
from logging import StreamHandler
from logging import Formatter
from logging import getLoggerClass
from logging import DEBUG, ERROR
from oriole_service.conf import Config

FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'


def logger():
    """ Create a standard logger. """

    Logger = getLoggerClass()

    class DebugLogger(Logger):
        def getEffectiveLevel(self):
            conf = Config().get('log_level', '')
            if conf == 'DEBUG':
                return DEBUG
            return Logger.getEffectiveLevel(self)

    class DebugHandler(StreamHandler):
        def emit(self, record):
            StreamHandler.emit(self, record)

    debug_handler = DebugHandler()
    debug_handler.setLevel(DEBUG)
    debug_handler.setFormatter(Formatter(FORMAT))

    logger = getLogger(__name__)

    del logger.handlers[:]
    logger.__class__ = DebugLogger
    logger.addHandler(debug_handler)
    logger.propagate = False

    return logger


class Log(object):
    """ Create a mongo logger.

    Returns::

        Collection

    Examples::

        from oriole_service.log import Log
        log = Log("config_in_cfg").get()
        result = log.insert_one({"count":1})
        result.acknowledged
    """

    def __init__(self, module=""):
        """ Require server info """

        conf = Config()['log'][module]
        self.log = ""
        self.host = conf['host']
        self.db = conf['db']
        self.tb = conf['tb']
        self._log = logger()

    def get(self):
        """ Return log handler """

        self._log.info("Connect %s.%s" % (self.host, self.db))
        self.conn = mogo.connect(self.db, self.host)
        self.log = self.conn[self.db][self.tb]
        if not self.log:
            self._log.error("Log connect: fail.")
        return self.log
