# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yekta_metrics']

package_data = \
{'': ['*']}

install_requires = \
['prometheus-client>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'yekta-metrics',
    'version': '2.3.8',
    'description': 'Yektanet Metrics Module',
    'long_description': None,
    'author': 'Sadegh Hayeri',
    'author_email': 'hayerisadegh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
