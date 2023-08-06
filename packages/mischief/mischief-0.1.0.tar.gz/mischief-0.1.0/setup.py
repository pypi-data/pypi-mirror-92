# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mischief', 'mischief.bin']

package_data = \
{'': ['*']}

install_requires = \
['colorama', 'requests']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['pymischief = mischief.bin.pymischief:main']}

setup_kwargs = {
    'name': 'mischief',
    'version': '0.1.0',
    'description': 'Another interface to haveibeenpwned.com',
    'long_description': '# Mischief\n\n# Required Libraries\n\n- requests\n- colorama\n\n# Example\n\nPlace a list of accounts (emails) into a json file array:\n\n```json\n[\n    "test@example.com"\n]\n```\n\nThen call `pymischief` and the file:\n\n```bash\n kevin@Logan bin $ ./pymischief.py test.json\n[test@example.com]========================\n 000webhost [14 million accounts total]\n   Domain: 000webhost.com\n   2015-03-01\n   Data still on web\n   Hack verified by website\n   Leaked data:\n     - Email addresses\n     - IP addresses\n     - Names\n     - Passwords\n 8tracks [7 million accounts total]\n   Domain: 8tracks.com\n   2017-06-27\n   Data still on web\n   Hack verified by website\n   Leaked data:\n     - Email addresses\n     - Passwords\n...\nPaste: test@example.com ==============\n  AdHocUrl: http://siph0n.in/exploits.php?id=4560\n  AdHocUrl: http://balockae.online/files/BlackMarketReloaded_users.sql\n  AdHocUrl: http://siph0n.in/exploits.php?id=7854\n  AdHocUrl: http://pxahb.xyz/emailpass/www.ironsudoku.com.txt\n  AdHocUrl: http://pxahb.xyz/emailpass/www.optimale-praesentation.de.txt\n  Pastebin: https://pastebin.com/01ywCrGV\n  QuickLeak: http://quickleak.se/QtPly6aE\n  Pastebin: https://pastebin.com/B8TeVHVt\n  Pastebin: https://pastebin.com/VvKhYPR0\n  Pastebin: https://pastebin.com/ktnvMJDH\n  Pastebin: https://pastebin.com/tJmdW6sp\n  Pastebin: https://pastebin.com/L730bR9a\n  Pastebin: https://pastebin.com/h2KJPWJ9\n  Pastebin: https://pastebin.com/0SqeEgZe\n  Pastebin: https://pastebin.com/tcHtWCFD\n  Pastebin: https://pastebin.com/yukVFztc\n...\n```\n\n# MIT License\n\n**Copyright (c) 2019 Kevin J. Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/mischief/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
