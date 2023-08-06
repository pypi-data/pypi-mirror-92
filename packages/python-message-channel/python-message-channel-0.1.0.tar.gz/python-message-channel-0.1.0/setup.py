# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['message_channel']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-message-channel',
    'version': '0.1.0',
    'description': 'Generic asynchronous message channel with routing by predicators',
    'long_description': '# message-channel\n\n![PyPI](https://img.shields.io/pypi/v/python-message-channel)\n![PyPI - License](https://img.shields.io/pypi/l/python-message-channel)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-message-channel)\n![Test](https://github.com/fixpoint/python-message-channel/workflows/Test/badge.svg)\n\n**UNDER DEVELOPMENT**\n',
    'author': 'Alisue',
    'author_email': 'lambdalisue@hashnote.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fixpoint/python-message-channel',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
