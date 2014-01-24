from __future__ import absolute_import
from docutils.core import publish_from_doctree, publish_doctree
from contextlib import contextmanager
from lovely.pyrest.rest import SERVICES
from pyramid import testing
from webtest import TestApp
from importlib import import_module
import unittest
import doctest
import os
import pprint
import json
import sys
import tempfile
import shutil
import sphinx.cmdline


project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
here = os.path.dirname(__file__)


DOC_CONF = """
extensions = ['lovely.pyrest.sphinx']
source_suffix = '.txt'
master_doc = 'index'
html_theme = 'pyramid'
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
    SERVICES.clear()
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


def get_app(module_str):
    # scans the defined module and returns
    # a TestApp

    # Settings can also be defined in a .ini file.
    settings = {
        'lovely.pyrest.jsonp.param_name': 'callback'
    }
    config = testing.setUp(settings=settings)
    module = import_module(module_str)
    # check if the module has an `includeme` method and call it
    # because the base route must be added
    if hasattr(module, 'includeme'):
        module.includeme(config)
    config.commit()
    config.scan(module)
    return TestApp(config.make_wsgi_app())


def setUp(test):
    test.globs['print_json'] = print_json
    test.globs['pprint'] = pprint.pprint
    test.globs['render_doc_node'] = render_doc_node
    test.globs['render_doc'] = render_doc
    test.globs['get_app'] = get_app


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
        create_suite('../../docs/sphinx.txt'),
        create_suite('../../docs/index.txt'),
    ))
    return s
