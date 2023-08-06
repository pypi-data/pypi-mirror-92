# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sapientacli']
install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'tqdm>=4.56.0,<5.0.0',
 'websockets>=8.1,<9.0']

entry_points = \
{'console_scripts': ['sapientacli = sapientacli:main']}

setup_kwargs = {
    'name': 'sapientacli',
    'version': '0.1.0',
    'description': 'A simple command line tool for usage of SAPIENTA API (https://sapienta.papro.org.uk)',
    'long_description': None,
    'author': 'James Ravenscroft',
    'author_email': 'ravenscroftj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
