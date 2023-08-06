# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['davidoc',
 'davidoc.apps',
 'davidoc.apps.services',
 'davidoc.apps.users',
 'davidoc.apps.utils',
 'davidoc.core',
 'davidoc.dataparsin']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy==1.4.0b1',
 'email-validator>=1.1.2,<2.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'psycopg2>=2.8.6,<3.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['doc = davidoc.app:doc']}

setup_kwargs = {
    'name': 'davidoc',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'arantesdv',
    'author_email': 'arantesdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
