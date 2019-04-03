# Oriole-Service 

[![](https://badges.gitter.im/zhouxiaoxiang/oriole-service.svg)](https://gitter.im/oriole-service/Lobby?utm_source=share-link&utm_medium=link&utm_campaign=share-link)

[【Chinese readme】](https://zhouxiaoxiang.top/2019/01/05/微服务快速开发/)

[【English readme】](https://github.com/zhouxiaoxiang/oriole-service/blob/master/README.md)

[【Code】](https://github.com/zhouxiaoxiang/oriole-service)

**The Zen of oriole: speed defines the winner.**

## Prerequisites

1. Install following packages

 - python >= 3.6
 - mongodb
 - mysql
 - rabbitmq
 - redis

2. Install oriole-service
```
  pip install oriole-service
```

## Add services.cfg

services.cfg

```
AMQP_URI:      pyamqp://test:test@127.0.0.1                  
database:      mysql://test:test@127.0.0.1/test?charset=utf8
test_database: mysql://test:test@127.0.0.1/test?charset=utf8
datasets:      redis://127.0.0.1/0
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

services/log.py

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

## Run log service
```
  o r log
```

## Run console
```
  o s
```
![](https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/run.gif)

## Halt log service
```
  o h log
```

## Create documents.
```
  o d
```

## Check online services

  You can run `o s` to do the same thing.

![](https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/check_service.gif)

## Create docker image.

Don't use it if you don't know docker at all before.

Create log_service image. 

```
  o b log
```
