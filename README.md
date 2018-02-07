# Oriole-Service

[![Join project](https://badges.gitter.im/zhouxiaoxiang/oriole-service.svg)](https://gitter.im/oriole-service/Lobby?utm_source=share-link&utm_medium=link&utm_campaign=share-link) [![Let's go](https://travis-ci.org/zhouxiaoxiang/oriole-service.svg?branch=master)](https://travis-ci.org/zhouxiaoxiang/oriole-service)

**Rapidly create services.**

## Prerequisites

1. Install following packages.

 - python >= 3.6
 - mongodb
 - mysql
 - rabbitmq
 - redis

2. Modify services.cfg in your project.

```
AMQP_URI:      ${RABBIT:pyamqp://test:test@127.0.0.1}                                 
database:      ${MYSQL:mysql://test:test@127.0.0.1/test?charset=utf8}
test_database: ${TEST_MYSQL:mysql://test:test@127.0.0.1/test?charset=utf8}
datasets:      ${REDIS:redis://127.0.0.1/0}
```

## Install

  cd <project>

  make

## Unit test

  o t <service>

## Run service

  o r <service>

## Run console

  o s

![](https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/run.gif)

## Halt service

  o h <service>

## Create docs

  o d

## Publish project

## Check

![](https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/check_service.gif)
