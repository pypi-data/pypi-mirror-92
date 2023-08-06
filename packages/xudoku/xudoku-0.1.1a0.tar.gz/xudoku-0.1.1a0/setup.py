# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xudoku']

package_data = \
{'': ['*']}

install_requires = \
['exact-cover>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'xudoku',
    'version': '0.1.1a0',
    'description': "Solve sudoku using an 'exact cover' algorithm.",
    'long_description': None,
    'author': 'Moy Easwaran',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
