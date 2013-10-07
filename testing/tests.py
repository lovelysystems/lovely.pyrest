# Shared Source Software
# Copyright (c) 2013, Lovely Systems GmbH

import unittest
import doctest
import requests
import sphinx.cmdline
import tempfile
import shutil
import os
from lovely.pyrest.tests import print_json
from contextlib import contextmanager
from webtest import TestApp
from pyramid import testing
from pprint import pprint
from lovely.pyrest.service import SERVICES

DOC_CONF = """
from lovely.documentation.sphinx_general import *
extensions = ['lovely.pyrest.sphinx']
source_suffix = '.txt'
master_doc = 'index'
html_theme = 'lovelysystems'
"""


@contextmanager
def _temp_dir():
    tmp = tempfile.mkdtemp()
    yield tmp
    shutil.rmtree(tmp)


def render_doc(rst_path):
    """ Renders a restructured Text file and returns the
        html output """

    # Remove all existing services
    del SERVICES[:]
    with _temp_dir() as tmp:
        out_dir = os.path.join(tmp, 'out')
        in_dir = os.path.join(tmp, 'in')
        os.mkdir(in_dir)
        # write the rst string to a file
        conf = DOC_CONF % dict(
            rst_file=rst_path
        )
        shutil.copyfile(rst_path, os.path.join(in_dir, 'index.txt'))
        conf_path = os.path.join(in_dir, 'conf.py')
        with file(conf_path, 'wb') as cf:
            cf.write(conf)
        sphinx_argv = ['sphinx-build', '-b', 'html',
                       in_dir, out_dir]
        sphinx.cmdline.main(sphinx_argv)
        index_path = os.path.join(out_dir, 'index.html')
        with open(index_path, 'r') as index:
            return index.read()


def get_app(module):
    # scans the defined module and returns
    # a TestApp
    config = testing.setUp(settings={'lovely.pyrest.jsonp': False})
    config.include('lovely.pyrest')
    config.scan(module)
    return TestApp(config.make_wsgi_app())


def setUp(test):
    test.globs['requests'] = requests
    test.globs['print_json'] = print_json
    test.globs['get_app'] = get_app
    test.globs['pprint'] = pprint
    test.globs['render_doc'] = render_doc
    pass


def tearDown(test):
    pass


def create_suite(testfile, layer=None, level=None,
                 tearDown=tearDown, setUp=setUp, cls=doctest.DocFileSuite):
    suite = cls(
        testfile, tearDown=tearDown, setUp=setUp,
        optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    if layer:
        suite.layer = layer
    if level:
        suite.level = level
    return suite


def test_suite():
    s = unittest.TestSuite((
        create_suite('../docs/index.txt'),
        create_suite('../docs/service.txt'),
        create_suite('../docs/validation.txt'),
        create_suite('../docs/sphinx.txt'),
    ))
    return s
