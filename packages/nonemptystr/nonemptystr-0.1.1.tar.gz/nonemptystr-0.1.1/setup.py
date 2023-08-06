# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonemptystr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nonemptystr',
    'version': '0.1.1',
    'description': 'Non-empty string',
    'long_description': '# nonemptystr\n\n[![PyPI](https://img.shields.io/pypi/v/nonemptystr)](https://pypi.org/project/nonemptystr/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nonemptystr)](https://pypi.org/project/nonemptystr/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![license](https://img.shields.io/github/license/nekonoshiri/nonemptystr)](https://github.com/nekonoshiri/nonemptystr/blob/main/LICENSE)\n\nNon-empty string.\n\n## Usage\n\n```Python\nfrom nonemptystr import EmptyString, nonemptystr\n\nname: nonemptystr = nonemptystr("John")\n\ntry:\n    name = nonemptystr("")\nexcept EmptyString:\n    print("The name is empty.")\n```\n\n## API\n\n### Module `nonemptystr`\n\n#### *class* `nonemptystr(obj: object)`\n\nSubclass of `str`.\nRaise `EmptyString` exception if `str(obj)` is empty string.\n\n#### *class* `EmptyString`\n\nSubclass of `ValueError`.\n\n',
    'author': 'Shiri Nekono',
    'author_email': 'gexira.halen.toms@gmail.com',
    'maintainer': 'Shiri Nekono',
    'maintainer_email': 'gexira.halen.toms@gmail.com',
    'url': 'https://github.com/nekonoshiri/nonemptystr',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
