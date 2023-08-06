# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['improvisers']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0', 'scipy>=1.5.4,<2.0.0', 'toposort>=1.5,<2.0']

setup_kwargs = {
    'name': 'improvisers',
    'version': '0.1.0',
    'description': 'Library for modeling improvisers in stochastic games.',
    'long_description': None,
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
