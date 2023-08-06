# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src',
 'src.core',
 'src.core.macro',
 'src.core.property',
 'src.core.selector',
 'src.core.variable',
 'src.exception',
 'src.util',
 'src.util.cli']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['main = src.util.cli.command:main',
                     'test = src.test:main']}

setup_kwargs = {
    'name': 'sqss',
    'version': '0.1.0',
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
