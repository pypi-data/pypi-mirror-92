# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['all_relative']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'colorama>=0.4.4,<0.5.0']

entry_points = \
{'console_scripts': ['all-relative = all_relative.main:main']}

setup_kwargs = {
    'name': 'all-relative',
    'version': '0.1.8',
    'description': 'cli tool to convert a static site to use only relative urls',
    'long_description': "# all-relative\n\nA command line tool to convert a static site to use only relative urls.\n\nRun it from the the directory which contains your generated static site to have it convert all urls in html and css to be relative to that dir or specify it as a cli argument.\n\nRelative urls leaves you with a portable website that doesn't care what path it is mounted at. `/`, `/olizilla/` `/ipfs/hash/`, `file://x/y/z/`, the lot, it don't care. This allows you to load the same static site via [IPFS](https://ipfs.io) or github pages, or the localfile system, as well as from the root of your custom domain. Relative urls are wonderful.\n\nThe command will **edit the files in place**, so it's best to run it on generated output that you can recreate if you need to. If you can't, be sure to take a back up of your site first.\n\n## Install\n\nInstall it with \n\n```console\n$ pip install all-relative\n```\n\nor run just it wihtout installing it via `pipx` [see here if you haven't heard about it](https://github.com/pipxproject/pipx)\n\n```console\n$ pipx all-relative\n```\n\n## Usage\n\nRun the command from the root directory of your static site.\n\n```console\n$ all-relative\n```\n\n# Inspired by [all-relative](https://github.com/olizilla/all-relative)",
    'author': 'Ivan Gonzalez',
    'author_email': 'scratchmex@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scratchmex/all-relative',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
