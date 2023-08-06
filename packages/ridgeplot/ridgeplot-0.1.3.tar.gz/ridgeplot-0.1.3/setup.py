# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ridgeplot']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.5,<2.0.0', 'plotly>=4.14.3,<5.0.0', 'statsmodels>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'ridgeplot',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Tomas Pereira de Vasconcelos',
    'author_email': 'tomas@tiqets.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
