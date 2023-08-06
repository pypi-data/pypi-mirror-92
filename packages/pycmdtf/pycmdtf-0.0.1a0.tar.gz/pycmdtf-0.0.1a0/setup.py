# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycmdtf', 'pycmdtf.actions', 'pycmdtf.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'colorlog>=4.7.2,<5.0.0',
 'deepmerge>=0.1.1,<0.2.0',
 'junitparser>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['pycmdtf = pycmdtf.cli:cli_main']}

setup_kwargs = {
    'name': 'pycmdtf',
    'version': '0.0.1a0',
    'description': 'PyCmdTF: Command Testing Framework',
    'long_description': None,
    'author': 'Peter Stanko',
    'author_email': 'peter.stanko0@gmail.com',
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
