# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonapy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jsonapy',
    'version': '0.1.0',
    'description': 'Library for dumping models into JSON:API',
    'long_description': None,
    'author': 'Guillaume Fayard',
    'author_email': 'guillaume.fayard@pycolore.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
