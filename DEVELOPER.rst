===========================
Sandboxed Development Setup
===========================

The following packages need to be installed::

    python27

On OSX those packages could be installed with macports::

    sudo port install python27

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
