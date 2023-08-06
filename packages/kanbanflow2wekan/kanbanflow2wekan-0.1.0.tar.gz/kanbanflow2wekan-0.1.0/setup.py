# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kanbanflow2wekan']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'kanbanflow2wekan',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mdiniz97',
    'author_email': 'marcosdinizpaulo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
