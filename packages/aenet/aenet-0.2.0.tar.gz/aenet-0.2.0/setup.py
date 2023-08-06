# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aenet']

package_data = \
{'': ['*']}

install_requires = \
['asgl>=1.0.5,<2.0.0',
 'cvxpy>=1.1.0,<2.0.0',
 'numpy>=1.0.0,<2.0.0',
 'scikit-learn>=0.24.0,<0.25.0']

setup_kwargs = {
    'name': 'aenet',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Shota Imaki',
    'author_email': 'shota.imaki@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
