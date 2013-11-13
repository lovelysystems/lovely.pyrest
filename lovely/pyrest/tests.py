from pprint import pprint
import unittest
import doctest
import json
import sys
from pyramid.request import Request
from lovely.pyrest.errors import Errors
from docutils.core import publish_from_doctree, publish_doctree


def print_json(js):
    try:
        d = json.loads(js)
    except ValueError:
        print >> sys.stderr, js
        raise
    print(json.dumps(d, indent=4, sort_keys=True))


def render_doc_node(node, writer_name='pseudoxml'):
    """ Renderers a docutils node """
    # Create an empty document
    doc = publish_doctree("")
    # append the node
    doc.children.append(node)
    # publish the document and return the output
    return publish_from_doctree(doc, writer_name=writer_name)


def create_request():
    request = Request({})
    request.errors = Errors()
    return request


def setUp(test):
    test.globs['pprint'] = pprint
    test.globs['create_request'] = create_request
    test.globs['print_json'] = print_json
    test.globs['render_doc_node'] = render_doc_node


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
        create_suite('__init__.txt'),
        create_suite('itests/service_definition.txt'),
        create_suite('itests/accept_catch_all.txt'),
        create_suite('sphinx/schema.txt'),
        create_suite('sphinx/validators.txt'),
        create_suite('sphinx/service.txt'),
    ))
    return s
