from oriole_service.app import *
import time
from datetime import date, datetime, timedelta


class UserService(App):
    """ Support all user operations.

    Example::

        from nameko.standalone.rpc import ClusterRpcProxy
        CONFIG = {"AMQP_URI":"pyamqp://guest:guest@localhost"}
        with ClusterRpcProxy(CONFIG) as services:
            result = services.user_service.add_user('God')
    """

    name = "user_service"
    log = RpcProxy("log_service")

    def __init__(self):
        self.init()

    @rpc
    def add_user(self, name):
        current_date = datetime.utcnow()
        current_time = int(time.time())

        user = Users()
        user.name = name
        user.add_time = current_date
        user.add_time_int = current_time

        self.log.add_log({"add_user": name})
        self.db.add(user)
        self.db.commit()
