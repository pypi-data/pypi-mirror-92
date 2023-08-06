# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xudoku']

package_data = \
{'': ['*']}

install_requires = \
['exact-cover>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['doctest = run_tests:run_doctest',
                     'test = run_tests:test']}

setup_kwargs = {
    'name': 'xudoku',
    'version': '0.2.0',
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
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
