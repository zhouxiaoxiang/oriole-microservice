# Oriole-Service 

[![](https://badges.gitter.im/zhouxiaoxiang/oriole-service.svg)](https://gitter.im/oriole-service/Lobby?utm_source=share-link&utm_medium=link&utm_campaign=share-link)

[【Chinese readme】](https://zhouxiaoxiang.top/zh-cn/microservice/)

[【English readme】](https://zhouxiaoxiang.top/microservice/)

**The Zen of oriole: speed defines the winner.**

## Prerequisites

1. Install following packages

 - mongodb
 - mysql
 - rabbitmq
 - redis
 - python3.6
 - libpython3.6

In ubuntu, you can use apt-get to install.
Python3.6 and libpython3.6 have been installed in Ubuntu >= 18.04.

2. Install oriole-service
```
  pip install oriole-service
```

## Add services.cfg

```
AMQP_URI:      pyamqp://test:test@127.0.0.1                  
database:      mysql://test:test@127.0.0.1/test?charset=utf8
test_database: mysql://test:test@127.0.0.1/test?charset=utf8
datasets:      redis://127.0.0.1
```
  
## Add orm

dao/\_\_init\_\_.py

```
from oriole_service.db import *

class Eric(Base):
    __tablename__ = 'eric_table'
    uid = Column(types.Integer(), primary_key=True, autoincrement=True)
    param = Column(types.Unicode(255), unique=None, default='')
```

## Add services/log.py

```
from oriole_service.app import *

class LogService(App):
    name = service_name(__file__)
    ver = "1.0.0"

    @rpc
    def add(self, params={"param": "eric"}):
        self.log.debug("# %s(%s)" % ("add", params))
        return self._o(params)
```

## run
```
  o r log
```

## monitor
```
  o s
```
![](https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/run.gif)

## document
```
  o d
```

## check

Run `o s` to do the same thing.

![](https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/check_service.gif)

## Create docker image

DONOT use it if you don't know docker at all before.

Create log\_service image.

```
  o b log
```
