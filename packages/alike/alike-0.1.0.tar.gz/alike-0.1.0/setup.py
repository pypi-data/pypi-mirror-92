# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['alike']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'alike',
    'version': '0.1.0',
    'description': 'Loose object comparison for python',
    'long_description': None,
    'author': 'Davis Kirkendall',
    'author_email': 'davis.e.kirkendall@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
