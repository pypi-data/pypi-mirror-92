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
    'version': '0.1.2',
    'description': 'Tools for the AppStore Connect API.',
    'long_description': '# appstore-tools\n\nTools for the AppStore Connect API.\n\nThis package is designed to provide a way to store AppStore data (descriptions, keywords, screenshots, previews, etc) in a `git` repo and publish changes from the command line or python script.\n\n## Install\n\n```zsh\npip install appstore-tools\n```\n\n## Usage\n\n```zsh\nappstore-tools [-h] [--version] action [args]\n```\n\nExamples:\n\n```zsh\n# List all apps under the app store account\nappstore-tools apps\n\n# Download the assets for an app\nappstore-tools download --bundle-id com.example.myapp --asset-dir myassets\n\n# Publish the assets for an app\nappstore-tools publish --bundle-id com.example.myapp --asset-dir myassets\n```\n\n## Usage Config\n\nMost actions will require authentication with the AppStore Connect API, as well as specifying which app to target.\n\nAll these parameters can be passed via command line argument, but for convenience, they (and any others) can also be loaded from a config file.\n\nUse the default config file path of `appstore_tools.config`, or specify another with `--config-file CONFIG_FILE`.\n\n```ini\n; appstore_tools.config\n; sample contents\nissuer-id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\nkey-id=XXXXXXXXXX\nkey-file=/home/me/AppStoreConnect_AuthKey_XXXXXXXXXX.p8\nbundle-id=com.example.myapp\n```\n\n## Code Usage\n\n```python\n# Import the package\nfrom appstore_tools import appstore\n\n# Get the auth credentials\nwith open("AuthKey.p8", "r") as file:\n    key = file.read()\n\nissuer_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"\nkey_id="XXXXXXXXXX"\n\n# Create an access token\naccess_token = appstore.create_access_token(\n    issuer_id=issuer_id, key_id=key_id, key=key\n)\n\n# Call the API\napps = appstore.get_apps(access_token=access_token)\n\n```\n\n## Source\n\nClone the source code\n\n```zsh\ngit clone https://github.com/bennord/appstore-tools.git\n```\n\nInstall dependencies\n\n```zsh\npoetry install\n```\n\nRun from within project environment\n\n```zsh\npoetry shell\nappstore-tools --version\n```\n',
    'author': 'Ben Nordstrom',
    'author_email': 'bennord@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bennord/appstore-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
