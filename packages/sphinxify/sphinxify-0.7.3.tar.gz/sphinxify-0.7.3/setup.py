#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

extras_require = \
{":python_version < '3.7'": ['dataclasses']}

entry_points = \
{'console_scripts': ['sphinxify = sphinxify:main']}

setup(name='sphinxify',
      version='0.7.3',
      description='Convert Javadoc to Sphinx docstrings.',
      author='David Vo',
      author_email='david@vovo.id.au',
      url='https://github.com/auscompgeek/sphinxify',
      py_modules=['sphinxify'],
      extras_require=extras_require,
      entry_points=entry_points,
      python_requires='>=3.6',
     )
