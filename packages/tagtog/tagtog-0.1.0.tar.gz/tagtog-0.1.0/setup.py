# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tagtog']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tagtog',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Juan Miguel Cejuela',
    'author_email': 'juanmi@tagtog.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
