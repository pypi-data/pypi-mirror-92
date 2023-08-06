# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyhexdump']

package_data = \
{'': ['*']}

install_requires = \
['colorama']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['astromechspeak = ttastromech.bin.astromechspeak:main']}

setup_kwargs = {
    'name': 'pyhexdump',
    'version': '0.5.1',
    'description': 'A python hex dump utility',
    'long_description': '.. figure:: https://raw.githubusercontent.com/walchko/pyhexdump/master/pics/hexdump.png\n\npyhexdump\n==============\n\nInstall\n--------\n\nThe preferred installation method is::\n\n\tpip install pyhexdump\n\nUsage\n---------\n\n::\n\n\tpyhexdump test.file\n\nor\n\n.. code-block:: python\n\n\tfrom pyhexdump import hexdump\n\n\ttest = bytearray(range(256)) + bytearray(range(256))\n\thexdump(test)\n\n\nMIT License\n--------------\n\n**Copyright (c) 2017 Kevin J. Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/pyhexdump/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
