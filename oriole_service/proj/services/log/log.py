from oriole_service.app import *
from oriole_service.log import Log, logger


class LogService(App):

    """ Support syslog.

    Example::

        from nameko.standalone.rpc import ClusterRpcProxy
        CONFIG = {"AMQP_URI":"pyamqp://guest:guest@localhost"}
        with ClusterRpcProxy(CONFIG) as services:
            result = services.log_service.add_log({"content": "info"})
    """

    name = "log_service"

    def __init__(self):
        self.init()

        # Standard log
        self._log = logger()

        # Mongo log
        self.log = Log("sysLog").get()

    @rpc
    def add_log(self, content):
        self._log.info("add log: %s" % content)
        result = self.log.insert_one(content)

        self._log.info("add log result: %s" % result.acknowledged)
        return result.acknowledged
