# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smc']

package_data = \
{'': ['*']}

install_requires = \
['pyserial']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

setup_kwargs = {
    'name': 'smc',
    'version': '0.5.2',
    'description': "A python driver library for Pololu's Simple Motor Controllers",
    'long_description': None,
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/smc/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
