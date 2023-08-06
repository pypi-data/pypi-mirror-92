# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['humplib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'humplib',
    'version': '0.1.1',
    'description': 'a hump to underline tool',
    'long_description': None,
    'author': 'huoyinghui',
    'author_email': 'yhhuo@yunjinginc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pydtools/humplib/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
