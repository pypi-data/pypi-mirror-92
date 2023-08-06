# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mindstorm']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18,<2.0', 'scipy>=1.4,<2.0']

setup_kwargs = {
    'name': 'mindstorm',
    'version': '0.3.0',
    'description': 'Mindstorm: Advanced analysis of neuroimaging data',
    'long_description': '# mindstorm\n[![PyPI version](https://badge.fury.io/py/mindstorm.svg)](https://badge.fury.io/py/mindstorm)\n[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4248136.svg)](https://doi.org/10.5281/zenodo.4248136)\n\nPackage for advanced neuroimaging analysis tools.\n',
    'author': 'Neal Morton',
    'author_email': 'mortonne@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mortonne/mindstorm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
