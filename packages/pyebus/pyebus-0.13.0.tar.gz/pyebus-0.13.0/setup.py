# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyebus', 'pyebus.cli']

package_data = \
{'': ['*']}

install_requires = \
['anytree>=2.8.0,<3.0.0']

entry_points = \
{'console_scripts': ['ebt = pyebus.cli:main']}

setup_kwargs = {
    'name': 'pyebus',
    'version': '0.13.0',
    'description': 'Pythonic Interface to EBUS Daemon (ebusd)',
    'long_description': '.. image:: https://badge.fury.io/py/pyebus.svg\n    :target: https://badge.fury.io/py/pyebus\n\n.. image:: https://img.shields.io/pypi/dm/pyebus.svg?label=pypi%20downloads\n   :target: https://pypi.python.org/pypi/pyebus\n\n.. image:: https://travis-ci.org/c0fec0de/pyebus.svg?branch=main\n    :target: https://travis-ci.org/c0fec0de/pyebus\n\n.. image:: https://readthedocs.org/projects/pyebus/badge/?version=latest\n    :target: https://pyebus.readthedocs.io/en/latest/?badge=latest\n\n.. image:: https://codeclimate.com/github/c0fec0de/pyebus.png\n    :target: https://codeclimate.com/github/c0fec0de/pyebus\n\n.. image:: https://img.shields.io/pypi/pyversions/pyebus.svg\n   :target: https://pypi.python.org/pypi/pyebus\n\n.. image:: https://img.shields.io/badge/code%20style-pep8-brightgreen.svg\n   :target: https://www.python.org/dev/peps/pep-0008/\n\n.. image:: https://img.shields.io/badge/code%20style-pep257-brightgreen.svg\n   :target: https://www.python.org/dev/peps/pep-0257/\n\nPythonic interface to [EBUSD](https://github.com/john30/ebusd).\n\n',
    'author': 'c0fec0de',
    'author_email': 'c0fec0de@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/c0fec0de/pyebus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
