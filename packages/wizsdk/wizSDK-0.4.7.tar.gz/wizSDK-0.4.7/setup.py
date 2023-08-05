# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wizsdk']

package_data = \
{'': ['*'], 'wizsdk': ['images/*']}

install_requires = \
['Sphinx>=3.4.3,<4.0.0',
 'asyncchain>=0.1.0,<0.2.0',
 'asyncio>=3.4.3,<4.0.0',
 'numpy>=1.19.1,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'simple_chalk>=0.1.0,<0.2.0',
 'wizwalker>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'wizsdk',
    'version': '0.4.7',
    'description': 'API for interacting with and making bots for wizard101',
    'long_description': '# WizAPI botting tool\n\n### Create powerful bots for Wizard101\n\nA wrapper for [WizWalker](https://pypi.org/project/wizwalker/) to create the bots _you_ want, right now.\n',
    'author': 'Underpaid Dev',
    'author_email': 'underpaiddev1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
