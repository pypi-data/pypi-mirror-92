# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['appstore_tools', 'appstore_tools.actions', 'appstore_tools.appstore']

package_data = \
{'': ['*']}

install_requires = \
['ConfigArgParse>=1.2.3,<2.0.0',
 'PyJWT>=2.0.1,<3.0.0',
 'Pygments>=2.7.4,<3.0.0',
 'argparse-color-formatter>=1.2.2,<2.0.0',
 'colorama>=0.4.4,<0.5.0',
 'cryptography>=3.3.1,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'tqdm>=4.56.0,<5.0.0']

entry_points = \
{'console_scripts': ['appstore-tools = appstore_tools:run']}

setup_kwargs = {
    'name': 'appstore-tools',
    'version': '0.1.0',
    'description': 'Tools for the AppStore Connect API.',
    'long_description': None,
    'author': 'Ben Nordstrom',
    'author_email': 'bennord@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
