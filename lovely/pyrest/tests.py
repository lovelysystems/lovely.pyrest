# Shared Source Software
# Copyright (c) 2013, Lovely Systems GmbH
from pprint import pprint
import unittest
import doctest
from pyramid.request import Request
from lovely.pyrest.errors import Errors


def create_request():
    request = Request({})
    request.errors = Errors()
    return request


def setUp(test):
    test.globs['pprint'] = pprint
    test.globs['create_request'] = create_request


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
        create_suite('service.txt'),
        create_suite('validation.txt'),
        create_suite('predicates.txt'),
        create_suite('views.txt'),
        create_suite('rest.txt'),
    ))
    return s
