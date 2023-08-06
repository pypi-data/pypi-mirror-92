# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['desdeo']

package_data = \
{'': ['*']}

install_requires = \
['desdeo-emo>=1.0.0,<2.0.0',
 'desdeo-mcdm>=1.0.0,<2.0.0',
 'desdeo-problem>=1.0.0,<2.0.0',
 'desdeo-tools>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'desdeo',
    'version': '1.1.1',
    'description': 'Open source framework for interactive multiobjective optimization.',
    'long_description': None,
    'author': 'Giovanni Misitano',
    'author_email': 'giovanni.a.misitano@jyu.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
