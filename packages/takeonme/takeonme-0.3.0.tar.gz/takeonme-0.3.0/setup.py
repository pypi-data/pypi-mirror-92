# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['takeonme', 'takeonme.aws', 'takeonme.gcp']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.55,<2.0.0',
 'click==7.1.2',
 'google-api-python-client>=1.12.8,<2.0.0',
 'google-auth>=1.24.0,<2.0.0']

entry_points = \
{'console_scripts': ['takeonme = takeonme.cli:cli']}

setup_kwargs = {
    'name': 'takeonme',
    'version': '0.3.0',
    'description': 'Enumerate resources vulnerable to takeover',
    'long_description': None,
    'author': 'SecOps',
    'author_email': 'secops+takeonme@mozilla.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
