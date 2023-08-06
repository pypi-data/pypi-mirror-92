# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane']

package_data = \
{'': ['*']}

install_requires = \
['arcane-core>=1.0.7,<2.0.0',
 'google-api-python-client==1.7.8',
 'oauth2client==4.1.2']

setup_kwargs = {
    'name': 'arcane-spreadsheet',
    'version': '0.1.1',
    'description': 'Package description',
    'long_description': '# Arcane spreadsheet\n\nUtility package to use google spreadsheet\n',
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
