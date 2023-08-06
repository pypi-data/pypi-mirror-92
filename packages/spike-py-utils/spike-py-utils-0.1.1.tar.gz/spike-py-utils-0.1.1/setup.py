# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spike_py_utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.5,<2.0.0']

setup_kwargs = {
    'name': 'spike-py-utils',
    'version': '0.1.1',
    'description': 'Assortment of datascience and data engineering utilities',
    'long_description': None,
    'author': 'cd',
    'author_email': 'cdagnino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
