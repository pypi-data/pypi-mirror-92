# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coveo_example_library']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'coveo-example-library',
    'version': '0.0.3',
    'description': 'coveo-python-oss example library',
    'long_description': None,
    'author': 'Jonathan Piché',
    'author_email': 'jpiche@coveo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
