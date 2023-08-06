# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xdr_parser',
 'xdr_parser.data_types',
 'xdr_parser.data_types.declarations',
 'xdr_parser.data_types.definitions',
 'xdr_parser.data_types.specifiers',
 'xdr_parser.data_types.specifiers.sub']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'xdr-parser',
    'version': '0.0.1.dev0',
    'description': 'A XDR parser.',
    'long_description': '# XDR-Parser',
    'author': 'overcat',
    'author_email': '4catcode@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/overcat/xdr-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
