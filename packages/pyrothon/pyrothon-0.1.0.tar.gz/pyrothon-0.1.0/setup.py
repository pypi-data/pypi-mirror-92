# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrothon']

package_data = \
{'': ['*']}

install_requires = \
['Pyrogram>=1.1.13,<2.0.0', 'Telethon>=1.19.0,<2.0.0']

setup_kwargs = {
    'name': 'pyrothon',
    'version': '0.1.0',
    'description': 'United. Forever.',
    'long_description': None,
    'author': 'JosXa',
    'author_email': 'info@josxa.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Autogram/pyrothon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
