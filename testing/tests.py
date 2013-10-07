# Shared Source Software
# Copyright (c) 2013, Lovely Systems GmbH

import unittest
import doctest
import requests
from lovely.pyrest.tests import print_json
from webtest import TestApp
from pyramid import testing
from pprint import pprint


def get_app(module):
    # scans the defined module and returns
    # a TestApp
    config = testing.setUp()
    config.include('lovely.pyrest')
    config.scan(module)
    return TestApp(config.make_wsgi_app())


def setUp(test):
    test.globs['requests'] = requests
    test.globs['print_json'] = print_json
    test.globs['get_app'] = get_app
    test.globs['pprint'] = pprint
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
        create_suite('../docs/jsonp.txt'),
    ))
    return s
