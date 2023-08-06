# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kernreg']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3,<4.0.0',
 'mypy-extensions>=0.4.3,<0.5.0',
 'numba>=0.52.0,<0.53.0',
 'numpy>=1.19.5,<2.0.0',
 'pandas>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'kernreg',
    'version': '0.0.1',
    'description': 'Tool for non-parametric curve fitting using local polynomials..',
    'long_description': None,
    'author': 'Sebastian Gsell',
    'author_email': 'sebastian.gsell93@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.9',
}


setup(**setup_kwargs)
