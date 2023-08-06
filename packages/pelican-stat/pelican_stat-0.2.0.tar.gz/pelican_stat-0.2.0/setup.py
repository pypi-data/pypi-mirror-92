# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican_stat']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.3,<4.0.0',
 'click>=7.1.2,<8.0.0',
 'pandas>=1.2.1,<2.0.0',
 'pelican==4.5.4',
 'plotly>=4.14.3,<5.0.0']

entry_points = \
{'console_scripts': ['pelican-stat = pelican_stat.__main__:main']}

setup_kwargs = {
    'name': 'pelican-stat',
    'version': '0.2.0',
    'description': 'Command line tool that generates pelican article statistics',
    'long_description': '[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pypi-stat](https://img.shields.io/pypi/v/pelican-stat)](https://img.shields.io/pypi/v/pelican-stat)\n\n# pelican_stat\n\ncli tool for generating pelican article statistics\n\n## Getting Started\n\n### Prerequisites\n* [pipx](https://github.com/pipxproject/pipx)\n\n## Usage\n\nAs I pin pelican to 4.5.4 for API consistency, I suggest using pipx (or any other virtual environment mechanism) to install this tool.\n\n```sh\npipx install pelican_stat\n```\n\nAfter installation, you can see the detail by add `--help` flag.\n\ne.g.,\n\n```sh\npelican-stat --help\n```\n\nor\n\n```sh\npelican-stat plot --help\n```\n\n## Contributing\nSee [Contributing](contributing.md)\n\n## Authors\nWei Lee <weilee.rx@gmail.com>\n\nCreated from [Lee-W/cookiecutter-python-template](https://github.com/Lee-W/cookiecutter-python-template/) version 0.6.1\n',
    'author': 'Wei Lee',
    'author_email': 'weilee.rx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
