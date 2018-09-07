Oriole-Service
==============

|image0| |image1|

`【Chinese
readme】 <https://github.com/zhouxiaoxiang/oriole-service/wiki>`__

`【English
readme】 <https://github.com/zhouxiaoxiang/oriole-service/blob/master/README.md>`__

`【Code】 <https://github.com/zhouxiaoxiang/oriole-service>`__

**The Zen of oriole: speed defines the winner.**

Prerequisites
-------------

1. Install following packages

-  python >= 3.6
-  mongodb
-  mysql
-  rabbitmq
-  redis

2. Install oriole-service

   ::

         pip install oriole-service

Add services.cfg
----------------

`services.cfg <https://github.com/zhouxiaoxiang/oriole-service/wiki/services.cfg>`__

Add services/log.py
-------------------

`services/log.py <https://github.com/zhouxiaoxiang/oriole-service/wiki/log.py>`__

Run log service
---------------

::

      o r log

Run console
-----------

::

      o s

.. figure:: https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/run.gif
   :alt: 

Halt log service
----------------

::

      o h log

Create documents.
-----------------

::

      o d

Publish log service
-------------------

Check online services
---------------------

 You can run ``o s`` to do the same thing.

.. figure:: https://github.com/zhouxiaoxiang/oriole-service/raw/master/docs/check_service.gif
   :alt: 

Make service as docker container
--------------------------------

Don't use it if you don't know what docker is.

::

      o b

.. |image0| image:: https://badges.gitter.im/zhouxiaoxiang/oriole-service.svg
   :target: https://gitter.im/oriole-service/Lobby?utm_source=share-link&utm_medium=link&utm_campaign=share-link
.. |image1| image:: https://travis-ci.org/zhouxiaoxiang/oriole-service.svg?branch=master
   :target: https://travis-ci.org/zhouxiaoxiang/oriole-service
