# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recap_utils']

package_data = \
{'': ['*']}

install_requires = \
['click-pathlib>=2020.3,<2021.0',
 'click>=7.0,<8.0',
 'deepl-pro>=0.1.4,<0.2.0',
 'recap-argument-graph>=0.1.36,<0.2.0',
 'tomlkit>=0.7,<0.8']

entry_points = \
{'console_scripts': ['recap-utils = recap_utils.app:cli']}

setup_kwargs = {
    'name': 'recap-utils',
    'version': '0.1.11',
    'description': '',
    'long_description': None,
    'author': 'Mirko Lenz',
    'author_email': 'info@mirko-lenz.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
