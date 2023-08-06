=====================
Quick Start Tutorial
=====================

Dependencies
=============

MorpCC requires following services for it to function correctly:

* postgresql database. 3 databases are needed, for following purpose:

  * main database - for MorpCC application tables

  * warehouse database - MorpCC provides a Through-The-Web (TTW) data model
    manager which allows creation of tables and managing data using the Web UI.
    Tables created by this feature will store its data in this database.

  * cache database - used by ``beaker`` for caching and session  

* rabbitmq message queue - used by background processing engine

Bootstrapping new project
===========================

MorpCC requires Python 3.7 or newer to run. Python 3.6 is also supported but
you will need to install ``dataclasses`` backport into your environment.

The recommended way to install morpfw is to use `buildout <http://www.buildout.org>`_,
skeleton that is generated using ``mfw-template``. Please head to
`mfw-template documentation <http://mfw-template.rtfd.org>`_ for tutorial.

Bootstrapping without ``mfw-template``
=======================================

If you prefer to use ``virtualenv``, or other methods, you can follow these
steps.

First, lets get ``morpfw`` & ``morpcc`` installed

.. code-block:: console

   $ pip install morpfw morpcc

If you are using buildout, version locks files are available at
``mfw_workspace`` repository: https://github.com/morpframework/mfw_workspace/tree/master/versions

Lets create an ``app.py``. 

.. literalinclude:: _code/app.py

``morpcc`` is built on ``morpfw`` which boot up application using a ``settings.yml`` file, so lets
create one. You will need a fernet key which have to be generated using following python code:

.. code-block:: console

   $ python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

Then lets create a ``settings.yml``

.. code-block:: yaml

   application:
      title: My First App
      class: app:App
      factory: morpcc.app:create_morpcc_app
      
   configuration:
      morpfw.authn.policy: morpcc.app:AuthnPolicy
      morpfw.secret.fernet_key: '<fernet-key>'
      morpfw.storage.sqlstorage.dburi:  'postgresql://postgres:postgres@localhost:5432/morpcc'
      morpfw.storage.sqlstorage.dburi.warehouse: 'postgresql://postgres:postgres@localhost:5432/morpcc_warehouse'
      morpfw.blobstorage.uri: 'fsblob://%(here)s/blobstorage'
      morpfw.beaker.session.type: ext:database
      morpfw.beaker.session.url: 'postgresql://postgres:postgres@localhost:5432/morpcc_cache'
      morpfw.beaker.cache.type: ext:database
      morpfw.beaker.cache.url: 'postgresql://postgres:postgres@localhost:5432/morpcc_cache'
      morpfw.celery:
         broker_url: 'amqps://guest:guest@localhost:5671/'
         result_backend: 'db+postgresql://postgres:postgres@localhost:5432/morpcc_cache'

You will then need to initialize database migration:

.. code-block:: console

   $ morpfw migration init migrations

Default alembic 
Afterwards, you can then start the application using:

.. code-block:: console

   $ morpfw -s settings.yml register-admin -u admin -e admin@localhost.local
   $ morpfw -s settings.yml start

This will start your project at http://localhost:5000/

Understanding core framework functionalities
=============================================

MorpCC is built on top of Morepath, so we suggest you head to `Morepath
Documentation <http://morepath.rtfd.org>`_ for guide on how to register your
own views, etc.

CRUD engine, resource type system and REST API engine for MorpCC is provided by
MorpFW. Head to `MorpFW documentation <http://morpframework.rtfd.org>`_ to
understand more on the type system used in MorpCC.

The templating language used is TAL, and we extensively use METAL for template
inheritance. Head to `Chameleon TAL/METAL Language Reference <https://chameleon.readthedocs.io/en/latest/reference.html>`_
and `Zope Page Template Reference <https://zope.readthedocs.io/en/latest/zope2book/AppendixC.html>`_
to understand more about TAL and METAL.

