=============
Lovely PyRest
=============

Lovely Pyrest provides helpers to build REST-Webservices with pyramid.

Features
========

    - raise a 405 if an unimplemented method is called on a servie
    - provides schema validation using validictory
    - raises correct errors if the `Accept` or `Content-Type` header doesn't match
    - sphinx extension to automatically generate service documentation

Documentation
=============

Take a look at the `documentation <http://http://lovelysystems.github.io/lovely.pyrest/>`_
for usage information.

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

Generating Documentation
========================

Before generating the new documentation make sure the `gh-pages` submodule is up-to-date::

    git submodule init

    git submodule update

To generate the new documentation run::

    ./bin/sphinx-html

The documentation is located in the `gh-pages` directory which points to the
`gh-pages` submodule.

Publish documentation
---------------------

To publish the documentation commit the changed files in the `gh-pages`
submodule::

    cd gh-pages

    git add <changed-files>

    git commit -m "updated documentation"

    git push origin gh-pages
