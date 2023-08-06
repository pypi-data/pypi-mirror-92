# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['juna']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'juna',
    'version': '0.1.0',
    'description': 'runescape utilities for python',
    'long_description': None,
    'author': 'Nico Hämäläinen',
    'author_email': 'selitys@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
