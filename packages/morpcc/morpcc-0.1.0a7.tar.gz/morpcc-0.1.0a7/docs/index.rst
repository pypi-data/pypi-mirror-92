.. Morp Control Center documentation master file, created by
   sphinx-quickstart on Wed Jan 16 20:31:28 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


===============================================
MorpCC: Meta-IMS For Rapid Prototyping
===============================================

Morp Control Center (MorpCC) is a meta information management system (meta-IMS)
built on top of `Morp Framework (morpfw) <http://morpframework.rtfd.org>`_ &
`Morepath <http://morepath.rtfd.org>`_.
It is designed to provide common components needed for the the development
of IMSes while allowing flexibility for developers to customize and override
the components.

Features
=========

* Responsive default UI based on `Gentelella
  <https://github.com/puikinsh/gentelella>`_ project

* Pluggable auth system

  * User, group & API key management system (SQLAlchemy based)

  * REMOTE_USER based authentication

* Content type framework and CRUD UI

* Pluggable CRUD storage backend

  * SQLAlchemy (default)
 
  * ElasticSearch

  * Dictionary based, in-memory

* Listing / search interface with JQuery DataTables server-side API

* Pluggable blob storage backend

  * Filesystem store (default)

* REST API through morpfw content type API engine with JWT based token

* Statemachine engine using PyTransitions through morpfw

* Overrideable components and templates through
  `morepath <http://morepath.rtfd.org>`_ & `dectate <http://dectate.rtfd.org>`_
  app inheritance

Documentation
==============

.. toctree::
   :maxdepth: 2

   introduction
   quickstart
   community

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
