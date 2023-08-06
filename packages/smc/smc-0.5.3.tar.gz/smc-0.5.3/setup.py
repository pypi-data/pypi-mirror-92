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
    'version': '0.5.3',
    'description': "A python driver library for Pololu's Simple Motor Controllers",
    'long_description': '![](https://raw.githubusercontent.com/MomsFriendlyRobotCompany/smc/master/docs/pics/smc.jpg)\n\n# Pololu Simple Motor Controller\n\n[![image](https://img.shields.io/pypi/v/smc.svg)](https://github.com/MomsFriendlyRobotCompany/smc)\n[![image](https://img.shields.io/pypi/l/smc.svg)](https://github.com/MomsFriendlyRobotCompany/smc)\n[![image](https://img.shields.io/pypi/pyversions/smc.svg)](https://pypi.python.org/pypi/smc/)\n\nThis is a python driver library for the Pololu series of Simple Motor\nControllers.\n\n## Install\n\n    pip install smc\n\n## Usage\n\n``` python\nfrom smc import SMC\nimport time\n\nmc = SMC(\'/dev/ttyUSB0\', 115200)\n# open serial port and exit safe mode\nmc.init()\n\n# drive using 12b mode\nmc.speed(1000)\ntime.sleep(3)\nmc.speed(-1000)\ntime.sleep(3)\n\n# drive using 7b mode\nmc.speed7b(100)\ntime.sleep(3)\nmc.speed7b(-100)\ntime.sleep(3)\n\n# and stop motor\nmc.stop()\n```\n\n## Board\n\n![](https://raw.githubusercontent.com/MomsFriendlyRobotCompany/smc/master/docs/pics/smc-back.jpg)\n\n![](https://raw.githubusercontent.com/MomsFriendlyRobotCompany/smc/master/docs/pics/smc-io.jpg)\n\n![](https://raw.githubusercontent.com/MomsFriendlyRobotCompany/smc/master/docs/pics/smc-wiring.jpg)\n\n## MIT License\n\n**Copyright (c) 2017 Kevin J. Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a\ncopy of this software and associated documentation files (the\n"Software"), to deal in the Software without restriction, including\nwithout limitation the rights to use, copy, modify, merge, publish,\ndistribute, sublicense, and/or sell copies of the Software, and to\npermit persons to whom the Software is furnished to do so, subject to\nthe following conditions:\n\nThe above copyright notice and this permission notice shall be included\nin all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS\nOR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\nMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.\nIN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY\nCLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,\nTORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE\nSOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
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
