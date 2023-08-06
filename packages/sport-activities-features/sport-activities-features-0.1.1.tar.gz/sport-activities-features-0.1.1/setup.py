# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sport_activities_features']

package_data = \
{'': ['*']}

install_requires = \
['geopy>=2.0.0,<3.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'tcxreader>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'sport-activities-features',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'iztokf',
    'author_email': 'iztokf@fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
