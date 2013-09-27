# Shared Source Software
# Copyright (c) 2013 Lovely Systems GmbH

import os
import re
import ConfigParser
from setuptools import setup, find_packages
from lovely.pyrest import VERSION


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


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'validictory',
    'rfc3987'
]

test_requires = requires + [
    'webtest'
]

setup(name='lovely.pyrest',
      version=VERSION,
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
      keywords='gate module paywall',
      packages=find_packages(),
      include_package_data=True,
      extras_require=dict(
          test=nailed_requires([
              'collective.xmltestreport',
              'webtest',
          ]),
      ),
      zip_safe=False,
      install_requires=requires,
      tests_require=test_requires,
      test_suite="lovely.pyrest",
      )
