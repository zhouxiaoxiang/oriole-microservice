# Oriole-Service

[![Join project](https://badges.gitter.im/zhouxiaoxiang/oriole-service.svg)](https://gitter.im/oriole-service/Lobby?utm_source=share-link&utm_medium=link&utm_campaign=share-link) [![Let's go](https://travis-ci.org/zhouxiaoxiang/oriole-service.svg?branch=master)](https://travis-ci.org/zhouxiaoxiang/oriole-service)

**Rapidly create services.**

## Prerequisites

-   python >= 3.6
-   mongodb
-   mysql
-   rabbitmq
-   redis

## Install

    pip install oriole-service

## Test

    o t

![](https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/test.gif)

## Run

    o r <service>

![](https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/run.gif)

## Halt

    o h <service>

## Document

    o d

![](https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/doc.gif)

## Check

![](https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/check_service.gif)


## Docker Base (Version: 1.13.1)

If you are not familar with docker,  skip this paragraph.
Startup your rabbitmq/mysql/redis, and use their address below.

- Create an auth_service.

```
docker containers run -e 'RABBIT=pyamqp://' \
                      -e 'MYSQL=mysql://'   \
                      -e 'REDIS=redis://'   \
                      zhouxiaoxiang/service
```

- Login.

```
from oriole_service.api import ClusterRpcProxy

with ClusterRpcProxy({'AMQP_URI':'pyamqp://'}) as s:
    s.auth_service.login({})
```
