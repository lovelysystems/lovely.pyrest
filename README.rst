=============
Lovely PyRest
=============

Lovely Pyrest provides helpers to build REST-Webservices with pyramid.

Fatures
=======

    - raise a 405 if an unimplemented method is called on a servie
    - provides schema validation using validictory
    - raises correct errors if the `Accept` or `Content-Type` header doesn't match

Development Setup
=================

For development setup instructions see:

    INSTALL.txt

Bootstrap and buildout
======================

Bootstrap with python 2.7::

    /opt/local/bin/python2.7 bootstrap.py

Run buildout::

    ./bin/buildout -N

Testing
=======

Tu run all the tests use::

    ./bin/test

For additional testrunner options run::

    ./bin/test --help
