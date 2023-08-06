# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['message_channel']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-message-channel',
    'version': '0.2.0',
    'description': 'Generic asynchronous message channel with routing by predicators',
    'long_description': "# message-channel\n\n![PyPI](https://img.shields.io/pypi/v/python-message-channel)\n![PyPI - License](https://img.shields.io/pypi/l/python-message-channel)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-message-channel)\n![Test](https://github.com/fixpoint/python-message-channel/workflows/Test/badge.svg)\n\nThis library provides a message channel object which subtract particular messages from mass of messages. It's like _group by_ of SQL or ReactiveX but for asynchronous reader.\n\n## Installation\n\n```\npip install python-message-channel\n```\n\n## Usage\n\nFor example, assume that you have a string stream which messages are prefixed by `a`, `b`, ... `e` and you'd like to split subchannels for messages prefixed by `b` or `d` like below.\n\n```\n=============================================\n---------------------------------> a:foo\n--------------------+\n--------------------|------------> c:foo\n--------------------|------------> d:foo\n--------------------|------------> e:foo\n====================|========================\nchannel             |\n                   =|========================\n                    +------------> b:foo\n                   ==========================\n                   subchannel `m.startswith('b')`\n```\n\nThis library is a tool for handling such situation.\nFirst, create a `Channel` instance from a steram reader and you can receive messages by\n`channel.recv()` method.\nIn this example, we use `asyncio.Queue` as a stream.\n\n```python\nimport asyncio\n\nfrom message_channel import Channel\n\nasync def main():\n    # Create original stream\n    stream = asyncio.Queue()\n\n    # Create stream reader\n    async def reader():\n        return await stream.get()\n\n    # Create stream channel\n    async with Channel(reader) as channel:\n        stream.put_nowait('a:foo')\n        stream.put_nowait('b:foo')\n        stream.put_nowait('c:foo')\n        stream.put_nowait('d:foo')\n        stream.put_nowait('e:foo')\n        assert (await channel.recv()) == 'a:foo'\n        assert (await channel.recv()) == 'b:foo'\n        assert (await channel.recv()) == 'c:foo'\n        assert (await channel.recv()) == 'd:foo'\n        assert (await channel.recv()) == 'e:foo'\n\n\nif __name__ == '__main__':\n    asyncio.run(main())\n```\n\nAnd you can _split_ the channel by `channel.split()` method by a predicator like\n\n```python\n    async with Channel(reader) as channel:\n        def predicator(m):\n            return m.startswith('b:')\n\n        async with channel.split(predicator) as sub:\n            stream.put_nowait('a:foo')\n            stream.put_nowait('b:foo')\n            stream.put_nowait('c:foo')\n            stream.put_nowait('d:foo')\n            stream.put_nowait('e:foo')\n            # sub receive messages starts from 'b:'\n            assert (await sub.recv()) == 'b:foo'\n            # channel (original) receive messages other than above\n            assert (await channel.recv()) == 'a:foo'\n            assert (await channel.recv()) == 'c:foo'\n            assert (await channel.recv()) == 'd:foo'\n            assert (await channel.recv()) == 'e:foo'\n```\n\n## API documentation\n\nhttps://fixpoint.github.io/python-message-channel/\n\npowered by [pdoc](https://pdoc3.github.io/pdoc/).\n\n## License\n\nDistributed under the terms of the [MIT License](./LICENSE)\n",
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
