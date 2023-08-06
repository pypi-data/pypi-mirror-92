# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloj']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cloj',
    'version': '0.1.1',
    'description': 'Clojure inspired helper functions',
    'long_description': '# Clojure inspired helper functions\n\nThis is a small library with Clojure inspired helper functions. It uses only the standard library, without any external dependencies. Should work on Python 3.6 and above.\n\nThe goal is to implement replicas of the Clojure funcs that I admire.\n\n## Installation\n\nWith [poetry](https://python-poetry.org/) (always recommended):\n```bash\npoetry add cloj\n```\n\nWith pip:\n```bash \npip install cloj\n```\n\nImplemented:\n* take/drop\n* some\n* nth, first, second, third, fourth, fifth, forty_second, last\n\nSome examples:\n\n```python\nfrom cloj import take, drop\n\ntake(3, [1, 2, 3, 4, 5])\n>> [1, 2, 3]\n\ndrop(3, [1, 2, 3, 4, 5])\n>> [4, 5]\n\ndrop (100, [1, 2, 3, 4, 5])\n>> []\n```\n\n```python\nfrom cloj import first, second, third, fourth, fifth, forty_second, last\n\nfirst([1, 2, 3])\n>> 1\n\nlast([1, 2, 3])\n>> 3\n\nfirst([])\n>> None\n```\n',
    'author': 'MB',
    'author_email': 'mb@blaster.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/licht1stein/cloj',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
