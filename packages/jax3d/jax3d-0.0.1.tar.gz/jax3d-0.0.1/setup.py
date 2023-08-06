# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jax3d']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jax3d',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Conchylicultor',
    'author_email': 'etiennefg.pot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
