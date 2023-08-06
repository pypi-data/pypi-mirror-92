===============
Introduction
===============

MorpCC aims to solve several common challenges when doing enterprise web
application development, which tend to require capabilities such as:

* Enterprise directory service (LDAP/AD) integration

* User, group and permission management

* Task scheduling for background jobs

* Customizable business rules logic

* Customizable / overrideable components and views to cater to sub/similar
  use-cases.

* Data might be stored in remote systems or APIs, not necessarily a database.

* Scalability to handle large data processing workload

* Corporate theming

* Mobile-ready / mobile integration

* State tracking and state management

* Fast turnaround time from business requirements to prototype application

* Activity tracking & analytics

* Messages & notifications

MorpCC, and its underlying framework, `MorpFW <http://morpframework.rtfd.org>`_
attempts to assist the challenges above through leveraging the component
engine provided by `Morepath <http://morepath.rtfd.org>`_ and 
`Dectate <http://dectate.rtfd.org>`_ to provide:

* Default admin+user UI which can be overridden easily, enabling agility in
  development by allowing developers to focus more on the data domain model
  first, rather than the repetive application bootstrapping tasks. 

* CRUD with pluggable storage engine, allowing flexibility in writing your
  own storage implementation

* State engine support, simplifying task of developing stage management of your
  data objects

* Pluggable user, group, permission and API key management.

* Standardized REST API interface for external integration.

* (TBD) Powerful theming capability through `diazo <http://docs.diazo.org>`_.

morpcc and morpfw design is highly influenced by `Plone <http://plone.org>`_
project. Unlike frameworks such as Django, Pyramid, and Flasks routing which
routes to views, morpcc/morpfw routing routes to an object/model publisher.
Views are attached to model and goes around with the model. 
This design gives the framework certain benefits:

* Views and view templates are highly reusable because as long as the model
  implements the attributes and methods the view queries, the view can be
  attached to the model.

* Views can be inherited by sub-models. You can create mixin interface classes
  and attach the views to it. Any models which inherits from the mixin will get
  the view.

* Views follows model and its sub-models. Whatever path the model is mounted,
  the views for the model will follow.


Underlying Frameworks & Libraries
==================================

MorpCC was built using the following frameworks & libraries to power it. So if
you need more detailed documentation on specific components that are not
covered here, please head to their documentation

* `Morepath <http://morepath.rtfd.org>`_ - Python web framework with superpowers

* `MorpFW <http://morpframework.rtfd.org>`_ - A REST API web framework built on
  top of Morepath.

* `Reg <http://reg.rtfd.org>`_ - Dispatching library similar to `Zope Component
  Architecture <https://zopecomponent.readthedocs.io>`_

* `Dectate <http://dectate.rtfd.org>`_ - Decorator based configuration system

* `SQLAlchemy <http://sqlalchemy.org>`_ - SQL abtraction library & ORM, used
  as the default storage engine.

* `Chameleon <http://chameleon.rtfd.org>`_ - Templating engine that implements
  `Zope Template Attribute Language (TAL) <https://chameleon.readthedocs.io/en/latest/reference.html>`_.

* `Rulez <https://github.com/morpframework/rulez>`_ - JSON based rules engine

* `PyTransitions <https://github.com/pytransitions/transitions>`_ - State machine
  engine for Python.

* `Celery <http://www.celeryproject.org/>`_ - Distributed task queue and job
  scheduling library for Python.

* `Gentelella <https://github.com/puikinsh/gentelella>`_ - Bootstrap 3 based
  admin template.


Entity Model
=============


.. image:: _static/entity-model.png


