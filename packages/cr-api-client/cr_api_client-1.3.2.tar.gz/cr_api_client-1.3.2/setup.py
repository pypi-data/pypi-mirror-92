# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cr_api_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0', 'ruamel.yaml>=0.16.10,<0.17.0']

entry_points = \
{'console_scripts': ['cyber_range = cr_api_client.cyber_range:main']}

setup_kwargs = {
    'name': 'cr-api-client',
    'version': '1.3.2',
    'description': 'CyberRange Amossys API Client',
    'long_description': None,
    'author': 'AMOSSYS',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
