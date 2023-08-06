# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfmini']

package_data = \
{'': ['*']}

install_requires = \
['pyserial']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

setup_kwargs = {
    'name': 'tfmini',
    'version': '0.2.0',
    'description': 'A driver for the TFmini LiDAR sold by Sparkfun',
    'long_description': '.. image:: https://raw.githubusercontent.com/MomsFriendlyRobotCompany/tfmini/master/tfmini.jpg\n\nTFmini\n========\n\nInstall\n----------\n\nInstall using ``pip``:\n\n::\n\n    pip install -U tfmini\n\nUsage\n------\n\nReading the sensor returns the range in meters.\n\n.. code-block:: python\n\n    from __future__ import division, print_function\n    import time\n    from tfmini import TFmini\n\n    # create the sensor and give it a port and (optional) operating mode\n    tf = TFmini(\'/dev/tty.usbserial-A506BOT5\', mode=TFmini.STD_MODE)\n\n    try:\n        print(\'=\'*25)\n        while True:\n            d = tf.read()\n            if d:\n                print(\'Distance: {:5}\'.format(d))\n            else:\n                print(\'No valid response\')\n            time.sleep(0.1)\n\n    except KeyboardInterrupt:\n        tf.close()\n        print(\'bye!!\')\n\n\n- ``TFmini(port, mode=5, retry=25)``: the constructor takes several inputs\n    - ``port``: serial port the sensor is connected too\n    - ``mode``: either standard (*default*) or decimal mode\n    - ``retry``: how many times the driver should search the serial port for the packet header. This only applies in standard mode.\n- ``read()``: in any mode, returns the distance in meters\n- ``TFmini.strength``: in standard mode, each packet contains the returned IR strength level. In decimal mode, this doesn\'t exist and is always set to -1.\n\nStandard (Packet) Mode\n-----------------------------\n\nIn this mode, a data packet is sent from the sensor:\n\n::\n\n    packet = [0x59, 0x59, distL, distH, strL, strH, reserved, integration time, checksum]\n\nWhere the first two bytes ``0x59, 0x59`` are the header and each packet has a\nchecksum to ensure the packet is valid data.\n\nDecimal (String) Mode\n----------------------------\n\nIn this mode, the sensor can sometimes returns an incorrect value because the\nASCII string was read wrong across the serial port. There is no error checking\nin this mode.\n\n.. code-block:: bash\n\n    Distance:  2.96\n    Distance:  2.96\n    Distance:  96.0 <<< Error\n    Distance:  2.95\n    Distance:  2.95\n    Distance:  2.96\n\nReferences\n-------------\n\n- `Sparkfun product page <https://www.sparkfun.com/products/14577>`_\n- `Manufacturer produce page <http://www.benewake.com/en/tfmini.html>`_\n\nMIT License\n============\n\n**Copyright (c) 2018 Kevin Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/tfmini/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
