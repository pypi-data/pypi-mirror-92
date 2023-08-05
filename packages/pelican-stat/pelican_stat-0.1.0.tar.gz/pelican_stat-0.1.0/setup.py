# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican_stat']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.3,<4.0.0', 'click>=7.1.2,<8.0.0', 'pelican==4.5.4']

entry_points = \
{'console_scripts': ['pelican-stat = pelican_stat.__main__:main']}

setup_kwargs = {
    'name': 'pelican-stat',
    'version': '0.1.0',
    'description': 'Command line tool that generates pelican article statistics',
    'long_description': '[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# pelican_stat\n\ncli tool for generating pelican article statistics\n\n## Getting Started\n\n### Prerequisites\n* [Python](https://www.python.org/downloads/)\n\n## Usage\n\n\n## Contributing\nSee [Contributing](contributing.md)\n\n## Authors\nWei Lee <weilee.rx@gmail.com>\n\n\nCreated from [Lee-W/cookiecutter-python-template](https://github.com/Lee-W/cookiecutter-python-template/) version 0.6.1\n',
    'author': 'Wei Lee',
    'author_email': 'weilee.rx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
