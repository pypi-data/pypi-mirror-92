# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jeejuh_dl']

package_data = \
{'': ['*']}

install_requires = \
['gazpacho>=1.1,<2.0', 'rich>=9.8.2,<10.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['jeejuh-dl = jeejuh_dl.main:app']}

setup_kwargs = {
    'name': 'jeejuh-dl',
    'version': '1.1',
    'description': 'Downloads links from jeejuh.com purchases',
    'long_description': '<div align="center">\n<img src="https://img.shields.io/pypi/v/jeejuh-dl"/>\n<img src="https://img.shields.io/pypi/pyversions/jeejuh-dl"/>\n<img src="https://img.shields.io/pypi/l/jeejuh-dl"/>\n<a href="https://twitter.com/mcohmi"><img src="https://img.shields.io/twitter/follow/mcohmi.svg?style=plastic"/></a><br>\n\n</div>\n\n# jeejuh-dl\n\nJeeJuh.com doesn\'t have a "download all" button which makes it a little annoying to have to click every stem for every beat, especially if you have multiple beats in one purchase. This CLI tool is written in Python and allows a user to point to their download page and grab all the files.\n\n**THIS TOOL IS NOT ASSOCIATED WITH OR ENDORSED BY JEEJUH.COM.**\n\n## Installation\n\nThe recommended method of installation is with [pipx](https://github.com/pipxproject/pipx).\n\n```\npipx install jeejuh-dl\n```\n\nHowever, you can install the normal way from PyPi with `python3 -m pip install jeejuh-dl`.\n\n## Usage\n\n`jeejuh-dl <URL>`\n\n```\nUsage: jeejuh-dl [OPTIONS] URL\n\nArguments:\n  URL  URL to jeejuh.com download page  [required]\n\nOptions:\n  --output DIRECTORY              [default: .]\n  -t, --threads INTEGER           Max number of concurrent downloads\n                                  [default: 5]\n\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n\n  --help                          Show this message and exit.\n```\n',
    'author': 'Leron Gray',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daddycocoaman/JeeJuh-Downloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
