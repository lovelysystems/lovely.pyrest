=============
Lovely PyRest
=============

Lovely Pyrest provides helpers to build REST-Webservices with pyramid.

Features
========

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

Note::

   Python shouldn't have installed any 3rd party packages

Testing
=======

To run all the tests use::

    ./bin/test

For additional testrunner options run::

    ./bin/test --help

Deploy Documentation
====================

The documentation is hosted at `github pages`. The submodule gh-pages contains
the static files. Ensure you have the submodule::

    git submodule init

    git submodule update

To generate the new documentation run::

    ./bin/sphinx-html

Move into the submodule::

    cd gh-pages

Commit the changed documentation::

    git commit -a -m "updated documentation

Push it::

    git push origin gh-pages
