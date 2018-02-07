# Oriole-Service 

[![](https://badges.gitter.im/zhouxiaoxiang/oriole-service.svg)](https://gitter.im/oriole-service/Lobby?utm_source=share-link&utm_medium=link&utm_campaign=share-link) [![](https://travis-ci.org/zhouxiaoxiang/oriole-service.svg?branch=master)](https://travis-ci.org/zhouxiaoxiang/oriole-service)

[Chinese readme](https://github.com/zhouxiaoxiang/oriole-service/wiki)

** Rapidly create services. **

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

  [services/log.py](https://github.com/zhouxiaoxiang/oriole-service/wiki/services.cfg)

## Add services/log.py

  [services/log.py](https://github.com/zhouxiaoxiang/oriole-service/wiki/log.py)

## Test log service
```
  o t log
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

## Publish log service

## Check online services

![](https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/check_service.gif)
