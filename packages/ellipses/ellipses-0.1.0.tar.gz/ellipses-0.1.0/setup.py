# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ellipses']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ellipses',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Enrico Borba',
    'author_email': 'enricozb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
