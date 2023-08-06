# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dolipy']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'dolipy',
    'version': '0.1.2',
    'description': 'A simple wrapper for dolibarr api',
    'long_description': None,
    'author': 'Dimitrios Strantsalis',
    'author_email': 'dstrants@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
