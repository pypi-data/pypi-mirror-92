# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xdrgen']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xdrgen',
    'version': '0.0.0.dev0',
    'description': '',
    'long_description': None,
    'author': 'overcat',
    'author_email': '4catcode@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
