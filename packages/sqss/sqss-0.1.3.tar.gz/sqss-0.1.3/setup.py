# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqss',
 'sqss.core',
 'sqss.core.macro',
 'sqss.core.property',
 'sqss.core.selector',
 'sqss.core.variable',
 'sqss.exception',
 'sqss.util',
 'sqss.util.cli']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['main = sqss.util.cli.command:main']}

setup_kwargs = {
    'name': 'sqss',
    'version': '0.1.3',
    'description': "pyqt's simple qss.",
    'long_description': None,
    'author': 'yijie',
    'author_email': 'yijie4188@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NWYLZW/sqss',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
