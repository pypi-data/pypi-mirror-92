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
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['saunadge = saunadge.server:cli']}

setup_kwargs = {
    'name': 'saunadge',
    'version': '0.1.0',
    'description': '',
    'long_description': '# saunadge\n\n![Build image](https://github.com/po3rin/saunadge/workflows/Build%20image/badge.svg)\n\nsaunadge lets you to generate sakatu(サ活/サウナ活動) badge. saunadge server aggregates from the data over [SAUNA-IKITAI](https://sauna-ikitai.com/).\n\n## Usage\n\n[![sakatsu badge](https://img.shields.io/endpoint.svg?url=https://saunadge-gjqqouyuca-an.a.run.app/api/v1/badge/46531&style=flat-square)](https://sauna-ikitai.com/saunners/46531)\n\n\n```sh\n[![sakatsu badge](https://img.shields.io/endpoint.svg?url=https://saunadge-gjqqouyuca-an.a.run.app/api/v1/badge/46531&style=flat-square)](https://sauna-ikitai.com/saunners/46531)\n```\n',
    'author': 'po3rin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/po3rin/saunadge',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
