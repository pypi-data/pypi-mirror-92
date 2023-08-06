# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grafiti']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'grafiti',
    'version': '0.1.0',
    'description': 'Automatic graph-based dependency resolution',
    'long_description': None,
    'author': 'Shiv Dhar',
    'author_email': 'shiv.dhar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
