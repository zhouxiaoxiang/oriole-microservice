Oriole-Service 服务框架
=======================

**Rapidly create services.**

快速创建微服务，打造企业软件平台。临渊羡鱼，不如退而结网，宏伟蓝图从这里开始。

|build|

Prerequisites 必要条件
----------------------

-  python3
-  mongodb
-  mysql
-  rabbitmq
-  redis

Install oriole. 安装
--------------------

::

      pip install oriole-service

Run unit test.  单元测试
------------------------

::

      o t

.. figure:: https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/test.gif
   :alt: 

Run a service. 启动服务
-----------------------

::

      o r <service>

.. figure:: https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/run.gif
   :alt: 

Generate documents. 创建文档
----------------------------

::

      o d

.. figure:: https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/doc.gif
   :alt: 

Run a client shell. 实网测试
----------------------------

::

      o s

.. figure:: https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/run.gif
   :alt: 

.. |build| image:: https://travis-ci.org/zhouxiaoxiang/oriole-service.png?branch=master
   :target: https://travis-ci.org/zhouxiaoxiang/oriole-service
