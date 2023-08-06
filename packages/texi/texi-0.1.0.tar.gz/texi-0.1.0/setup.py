# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['texi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'texi',
    'version': '0.1.0',
    'description': 'texi',
    'long_description': None,
    'author': 'Yevgnen Koh',
    'author_email': 'wherejoystarts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
