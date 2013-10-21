=============
Lovely PyRest
=============

Lovely Pyrest is an extension for
`Pyramid <http://www.pylonsproject.org/projects/pyramid/about>`_ to easily create
REST-Services. It provides functionallity to define service endpoints with the
following features:

Features
========

    - Sphinx extension to automatically generate documentation
    - It's possible to get help information of every endpoint
    - Schema-validation based on `jsonschema <http://json-schema.org/>`_
    - returns correct error codes if request method is not supportet or `Accept`-
      or `Content-Type`-Headers don't match

Documentation
=============

Take a look at the `documentation <http://lovelysystems.github.io/lovely.pyrest/>`_
for usage information.

Installation
============

Installing via pip
------------------

To install lovely.pyrest via `pip <https://pypi.python.org/pypi/pip>`_ use
the following command::

    $ pip install lovely.pyrest

To update use::

    $ pip install -U lovely.pyrest

Installing via easy_install
---------------------------

If you prefer easy_install which is provided by
`setuptools <https://pypi.python.org/pypi/setuptools/1.1>`_
use the following command::

    $ easy_install lovely.pyrest

To update use::

    $ easy_install -U lovely.pyrest


Development Setup
=================

For development setup instructions see:

    DEVELOPER.rst
