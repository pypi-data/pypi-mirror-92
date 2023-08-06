# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grafiti']

package_data = \
{'': ['*']}

install_requires = \
['icecream>=2.0.0,<3.0.0', 'pdbpp>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'grafiti',
    'version': '0.1.1',
    'description': 'Automatic graph-based dependency resolution',
    'long_description': "#########\ngrafiti\n#########\n\nWelcome to grafiti's documentation!\n\n",
    'author': 'Shiv Dhar',
    'author_email': 'shiv.dhar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
