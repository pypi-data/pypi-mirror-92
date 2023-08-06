# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uniset', 'uniset._category']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'uniset',
    'version': '0.1.0',
    'description': 'Pre-generated sets of Unicode code points',
    'long_description': '[![Build Status](https://github.com/hukkinj1/uniset/workflows/Tests/badge.svg?branch=master)](https://github.com/hukkinj1/uniset/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)\n[![codecov.io](https://codecov.io/gh/hukkinj1/uniset/branch/master/graph/badge.svg)](https://codecov.io/gh/hukkinj1/uniset)\n[![PyPI version](https://img.shields.io/pypi/v/uniset)](https://pypi.org/project/uniset)\n\n# uniset\n\n> Pre-generated sets of Unicode code points\n\n`uniset` is a module containing `frozenset`s of Unicode code points (characters).\n\n## API\n\n### Categories\n\nThe module includes a set for all Unicode categories and subcategories except the main category "C" (other)\nand its subcategories "Co" (private use) and "Cn" (not assigned).\n\nExample:\n\n```python\nimport uniset\n\n# The letter "A" is in category "L" (letters)\nassert "A" in uniset.L\n# The letter "A" is also in category "Lu" (uppercase letters)\nassert "A" in uniset.Lu\n```\n\n### Whitespace\n\n`uniset.WHITESPACE` contains all Unicode whitespace characters.\n`uniset.WHITESPACE` is a union of ASCII whitespace characters and the Unicode category "Zs".\n\n```python\nimport uniset\n\nassert " " in uniset.WHITESPACE\n```\n\n### Punctuation\n\n`uniset.PUNCTUATION` contains all Unicode punctuation letters.\n`uniset.PUNCTUATION` is a union of ASCII punctuation characters and the Unicode category "P".\n\n```python\nimport uniset\n\nassert "." in uniset.PUNCTUATION\n```\n\n## Alternatives\n\n[`unicategories`](https://gitlab.com/ergoithz/unicategories) also provides access to Unicode categories.\nThe implementation is based on "range groups" and iterators, and should be faster and more memory efficient than `uniset` for inclusion checks.\n\nIf you need the `frozenset` API (unions, intersections, etc.), or the sets beyond Unicode categories (whitespace, punctuation), use `uniset`.\nOtherwise `unicategories` is the better option.\n',
    'author': 'Taneli Hukkinen',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/uniset',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
