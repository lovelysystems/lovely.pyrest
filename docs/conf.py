import os
import re

# inject the VERSION constant used below
# This can be used because the build script updates the version number before
# building the RPM.
versionf_content = open("../lovely/pyrest/__init__.py").read()
version_rex = r'^__version__ = [\'"]([^\'"]*)[\'"]$'
m = re.search(version_rex, versionf_content, re.M)
if m:
    VERSION = m.group(1)
else:
    raise RuntimeError('Unable to find version string')


def read(path):
    return open(os.path.join(os.path.dirname(__file__), path)).read()

# The suffix of source filenames.
source_suffix = '.txt'

# The master toctree document.
master_doc = 'index'
html_use_modindex = False
html_use_index = False

nitpicky = True

# load doctest extension to be able to setup testdata in the documentation that
# is hidden in the generated html (by using .. doctest:: :hide:)
extensions = ['sphinx.ext.doctest']

# General information about the project.
project = u'lovely.pyrest'
copyright = u'2013, Lovely Systems GmbH'

version = release = VERSION
exclude_patterns = ['lovely.pyrest.egg-info', 'parts', 'checkouts']

html_theme = 'pyramid'
