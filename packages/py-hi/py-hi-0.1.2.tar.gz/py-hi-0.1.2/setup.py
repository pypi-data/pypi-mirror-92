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
    'version': '0.1.2',
    'description': 'hi is a tiny cli program that send benchmark request to almost everything based on asyncio',
    'long_description': '# hi\n\nhi is a tiny cli program that send benchmark request to "almost" everything. note that it\'s inspired by [rakyll/hey](https://github.com/rakyll/hey) and implemented by python/asyncio\n\n## Install\n\n `pip install py-hi`\n\n## Usage\n\n* say hi to github\n\n `hi https://github.com`\n\n* you will see\n\n``` bash\n➜ hi https://github.com\n\nSend request to https://github.com\n\nSummary:\nTotal:          6.327 secs\nSlowest:        6.297 secs\nFastest:        1.447 secs\nAverage:        4.388 secs\nRequests/sec:   31.611\n\nStatus code distribution:\n[200]        200 responses\n```\n\n## TODO\n\n* more send flag\n* request benchmark through shadowsocks\n',
    'author': 'Ehco1996',
    'author_email': 'zh19960202@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
