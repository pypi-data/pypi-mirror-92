Installing
============

You will need Visual Studio Code to make use of a number of convenience helpers
that have been preconfigured for the development of MorpCC. If you dont want to
use VSCode, read up ``.vscode/tasks.json`` for the common tasks. 

Checkout from git::

    git clone https://github.com/morpframework/morpcc.git

Load the directory with VSCode::

    code morpcc

Building
==========

To build, in VSCode command prompt, **Tasks: Run Task > Build Project**. This will trigger
buildout to build the project.

Starting Demo CMS
=====================

``morpcc.tests.democms`` includes a demo application for testing/development
of the platform. You will need to setup following databases on your local
PostgreSQL installation:

* morpcc_democms
* morpcc_democms_warehouse

Configuration of the democms application resides in
``morpcc/tests/democms/settings.yml``

You will need to generate an alembic migration script to initialize your
database. We decided not to include default migration scripts so that it is
easier for devs to customize migration scripts to suit their own needs. 

To generate alembic migration, in VSCode command prompt, ``Tasks: Run Task >
Generate Migrations``.

To initialize database, in VSCode command prompt, ``Tasks: Run Task > Update
database``

To create initial admin user, in VSCode command prompt, ``Tasks: Run Task >
Create default admin user (admin:admin)``

To start, in VSCode, press F5 or on the window menu, ``Debug > Start Debugging``

To run unit tests, in VSCode command prompt, ``Tasks: Run Task > Test Project``

Demo CMS shall be running at http://127.0.0.1:5000

Contacting The Author
======================

Come over to https://t.me/morpfw 
