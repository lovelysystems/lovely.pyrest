# Shared Source Software
# Copyright (c) 2013 Lovely Systems GmbH

import os
import re
import ConfigParser
from setuptools import setup, find_packages


def get_versions():
    """picks the versions from version.cfg and returns them as dict"""
    versions_cfg = os.path.join(os.path.dirname(__file__), 'versions.cfg')
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.readfp(open(versions_cfg))
    return dict(config.items('versions'))


def nailed_requires(requirements, pat=re.compile(r'^(.+)(\[.+\])?$')):
    """returns the requirements list with nailed versions"""
    versions = get_versions()
    res = []
    for req in requirements:
        if '[' in req:
            name = req.split('[', 1)[0]
        else:
            name = req
        if name in versions:
            res.append('%s==%s' % (req, versions[name]))
        else:
            res.append(req)
    return res


def read(path):
    return open(os.path.join(os.path.dirname(__file__), path)).read()
versionf_content = open("lovely/pyrest/__init__.py").read()
version_rex = r'^__version__ = [\'"]([^\'"]*)[\'"]$'
m = re.search(version_rex, versionf_content, re.M)
if m:
    version = m.group(1)
else:
    raise RuntimeError('Unable to find version string')


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'gevent',
    'pyramid',
    'validictory',
    'rfc3987'
]

test_requires = requires + [
    'webtest',
    'collective.xmltestreport',
    'requests'
]

setup(name='lovely.pyrest',
      version=version,
      description='REST Framework for pyramids',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Lovely Systems',
      author_email='office@lovelysystems.com',
      url='https://github.com/lovelysystems/lovely.pyrest',
      keywords='pyramid rest framework',
      packages=find_packages(),
      namespace_packages=['lovely'],
      include_package_data=True,
      extras_require=dict(
          test=nailed_requires(test_requires),
      ),
      zip_safe=False,
      install_requires=requires,
      tests_require=test_requires,
      test_suite="lovely.pyrest",
      )
