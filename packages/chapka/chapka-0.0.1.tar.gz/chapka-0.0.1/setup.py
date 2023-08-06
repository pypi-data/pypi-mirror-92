# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chapka']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chapka',
    'version': '0.0.1',
    'description': 'Clickhouse Query Builder and ORM',
    'long_description': None,
    'author': 'Alain BERRIER',
    'author_email': 'alain.berrier@outlook.com',
    'maintainer': 'Alain BERRIER',
    'maintainer_email': 'alain.berrier@outlook.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
