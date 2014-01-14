from webtest import TestApp
from pyramid import paster
from docutils.core import publish_from_doctree, publish_doctree
import unittest
import doctest
import os
import pprint
import requests
import json
import sys


project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
here = os.path.dirname(__file__)

#conf = os.path.join(here, 'testing', 'testing.ini')
#app = paster.get_app(conf, 'main')

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


def setUp(test):
#    testapp = TestApp(app)
#    test.globs['browser'] = testapp
    test.globs['print_json'] = print_json
    test.globs['pprint'] = pprint.pprint
    test.globs['render_doc_node'] = render_doc_node
#    test.globs['registry'] = testapp.app.registry


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
        create_suite('rest.rst'),
        create_suite('validation.rst'),
        create_suite('sphinx/service.txt'),
    ))
    return s
