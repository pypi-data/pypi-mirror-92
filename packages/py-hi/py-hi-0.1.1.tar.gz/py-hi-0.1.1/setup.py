# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['hi']
install_requires = \
['aiohttp>=3.7.3,<4.0.0', 'rich>=9.8.2,<10.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['hi = hi:main']}

setup_kwargs = {
    'name': 'py-hi',
    'version': '0.1.1',
    'description': 'hi from asyncio',
    'long_description': None,
    'author': 'Ehco1996',
    'author_email': 'zh19960202@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
