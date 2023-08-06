# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datacker', 'datacker.tests']

package_data = \
{'': ['*'], 'datacker.tests': ['notebooks/*']}

install_requires = \
['docker>=4.4.1,<5.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['datacker = datacker.cli:app']}

setup_kwargs = {
    'name': 'datacker',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Cristóbal Carnero Liñán',
    'author_email': 'ccarnerolinan@gmail.com',
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
