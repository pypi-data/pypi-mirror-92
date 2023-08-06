# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['voicegen']

package_data = \
{'': ['*']}

install_requires = \
['pytils==0.3', 'requests==2.25.1', 'sox==1.4.1']

setup_kwargs = {
    'name': 'voicegen',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Andrei Murashev',
    'author_email': 'muraigtor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
