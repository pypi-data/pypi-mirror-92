# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xdr_parser', 'xdr_parser.data_types']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'xdr-parser',
    'version': '0.0.0.dev0',
    'description': 'Parse XDR into AST.',
    'long_description': None,
    'author': 'overcat',
    'author_email': '4catcode@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
