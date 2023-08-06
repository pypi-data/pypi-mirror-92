# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysabertooth']

package_data = \
{'': ['*']}

install_requires = \
['pyserial']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

setup_kwargs = {
    'name': 'pysabertooth',
    'version': '0.4.0',
    'description': "A python driver library for Dimension Engineering's Sabertooth Motor Controllers",
    'long_description': '.. figure:: https://raw.githubusercontent.com/MomsFriendlyRobotCompany/pysabertooth/master/docs/pics/Sabertooth2x32Big.jpg\n\t:target: https://www.dimensionengineering.com/products/sabertooth2x32\n\n\nPySabertooth\n==============\n\n\n.. image:: https://img.shields.io/pypi/l/pysabertooth.svg\n\t:target: https://github.com/MomsFriendlyRobotCompany/pysabertooth\n.. image:: https://img.shields.io/pypi/pyversions/pysabertooth.svg\n\t:target: https://github.com/MomsFriendlyRobotCompany/pysabertooth\n.. image:: https://img.shields.io/pypi/wheel/pysabertooth.svg\n\t:target: https://github.com/MomsFriendlyRobotCompany/pysabertooth\n.. image:: https://img.shields.io/pypi/v/pysabertooth.svg\n\t:target: https://github.com/MomsFriendlyRobotCompany/pysabertooth\n\n\nInstall\n----------\n\n::\n\n\tpip install pysabertooth\n\nUsage\n--------\n\n.. code-block:: python\n\n\tfrom pysabertooth import Sabertooth\n\n\tsaber = Sabertooth(\'/dev/tty.usbserial\', baudrate=115200, address=128, timeout=0.1)\n\n\t# drive(number, speed)\n\t# number: 1-2\n\t# speed: -100 - 100\n\tsaber.drive(1, 50)\n\tsaber.drive(2, -75)\n\tsaber.stop()\n\n\nMIT License\n-------------\n\n**Copyright (c) 2017 Kevin J. Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/pysabertooth/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
