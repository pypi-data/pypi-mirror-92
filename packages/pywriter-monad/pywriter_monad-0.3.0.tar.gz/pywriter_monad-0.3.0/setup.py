# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['writer']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.6'],
 ':python_version < "3.8"': ['typing-extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'pywriter-monad',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Yohei Tamura',
    'author_email': 'tamuhey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
