# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['saunadge']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=1.1.2,<2.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'gunicorn>=20.0.4,<21.0.0',
 'lxml>=4.6.2,<5.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['saunadge = saunadge.server:cli']}

setup_kwargs = {
    'name': 'saunadge',
    'version': '0.2.1',
    'description': 'saunadge lets you to generate sakatsu(サ活/サウナ活動) badge. saunadge server aggregates from the data over',
    'long_description': None,
    'author': 'po3rin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/po3rin/saunadge',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
