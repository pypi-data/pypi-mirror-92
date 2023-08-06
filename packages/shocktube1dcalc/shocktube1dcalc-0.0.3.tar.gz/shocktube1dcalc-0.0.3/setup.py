# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shocktube1dcalc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shocktube1dcalc',
    'version': '0.0.3',
    'description': '1D shocktube caculator to provide analytic solutions',
    'long_description': None,
    'author': 'Taihsiang Ho (tai271828)',
    'author_email': 'tai271828@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
