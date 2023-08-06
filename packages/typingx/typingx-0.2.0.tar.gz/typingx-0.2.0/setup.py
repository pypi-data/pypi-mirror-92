# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typingx']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.9"': ['typing_extensions>=3.7.4.3,<4.0.0.0']}

setup_kwargs = {
    'name': 'typingx',
    'version': '0.2.0',
    'description': 'Extend typing package functionalities',
    'long_description': None,
    'author': 'Eric Jolibois',
    'author_email': 'em.jolibois@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PrettyWood/typingx',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
