# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tagtog']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tagtog',
    'version': '0.1.1',
    'description': 'Python library & CLI to interact with tagtog APIs & datasets',
    'long_description': 'Just getting started ;-)\n\nMore info at [tagtog.net](https://www.tagtog.net)\n',
    'author': 'tagtog team',
    'author_email': 'info@tagtog.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tagtog/pytagtog',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
