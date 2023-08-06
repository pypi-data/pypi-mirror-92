# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['offshore']

package_data = \
{'': ['*']}

install_requires = \
['portalocker>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'offshore',
    'version': '0.1.1',
    'description': 'Simple, ergonomic data persistence for Python.',
    'long_description': None,
    'author': 'Phil Demetriou',
    'author_email': 'inbox@philonas.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kpdemetriou/offshore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
