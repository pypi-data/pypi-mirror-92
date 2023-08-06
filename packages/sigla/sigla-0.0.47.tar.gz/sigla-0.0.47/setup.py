# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigla',
 'sigla.classes',
 'sigla.classes.nodes',
 'sigla.classes.outputs',
 'sigla.cli',
 'sigla.helpers',
 'sigla.tests']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'configparser>=5.0.1,<6.0.0',
 'flake8>=3.8.4,<4.0.0',
 'keyring>=22.0.1,<23.0.0',
 'pretty-errors>=1.2.19,<2.0.0',
 'pydash>=4.9.1,<5.0.0',
 'pytest-cov>=2.11.1,<3.0.0',
 'pytest>=6.2.1,<7.0.0',
 'python-frontmatter>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['sigla = sigla.cli.cli:cli']}

setup_kwargs = {
    'name': 'sigla',
    'version': '0.0.47',
    'description': '',
    'long_description': None,
    'author': 'mg santos',
    'author_email': 'mauro.goncalo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
