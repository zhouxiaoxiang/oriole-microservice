# Oriole-Service 

[![](https://badges.gitter.im/zhouxiaoxiang/oriole-service.svg)](https://gitter.im/oriole-service/Lobby?utm_source=share-link&utm_medium=link&utm_campaign=share-link) [![](https://travis-ci.org/zhouxiaoxiang/oriole-service.svg?branch=master)](https://travis-ci.org/zhouxiaoxiang/oriole-service)

[【Chinese readme】](https://github.com/zhouxiaoxiang/oriole-service/wiki)

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

  [services.cfg](https://github.com/zhouxiaoxiang/oriole-service/wiki/services.cfg)

## Add services/log.py

  [services/log.py](https://github.com/zhouxiaoxiang/oriole-service/wiki/log.py)

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

OK, now you can deploy it into kubernetes.
