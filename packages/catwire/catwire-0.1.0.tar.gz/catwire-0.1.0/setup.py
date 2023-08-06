# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['catwire']

package_data = \
{'': ['*']}

install_requires = \
['kaitaistruct>=0.9,<0.10']

setup_kwargs = {
    'name': 'catwire',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Johannes K Becker',
    'author_email': 'jkbecker@bu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
