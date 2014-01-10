import os
import re
import ConfigParser
from setuptools import setup, find_packages

import lovely.pyrest

VERSION = lovely.pyrest.VERSION

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


here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.rst')).read()
changes = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'gevent',
    'pyramid',
    'validictory',
    'docutils',
]

test_requires = requires + [
    'webtest',
    'collective.xmltestreport',
    'requests',
    'sphinx',
]

setup(name='lovely.pyrest',
      version=VERSION,
      description='rest framework for pyramids',
      long_description=readme + '\n\n' + changes,
      classifiers=[
          "programming language :: python",
          "framework :: pyramid",
          "topic :: internet :: www/http",
          "topic :: internet :: www/http :: wsgi :: application",
      ],
      author='lovely systems',
      author_email='office@lovelysystems.com',
      url='https://github.com/lovelysystems/lovely.pyrest',
      keywords='pyramid rest framework',
      license='apache license 2.0',
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
