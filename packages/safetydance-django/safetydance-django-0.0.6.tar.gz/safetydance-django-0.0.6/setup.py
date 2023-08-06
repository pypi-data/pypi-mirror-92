# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['safetydance_django']

package_data = \
{'': ['*']}

install_requires = \
['djangorestframework>=3.12.2,<4.0.0']

setup_kwargs = {
    'name': 'safetydance-django',
    'version': '0.0.6',
    'description': 'A collection of safetydance_test steps for BDD testing of Django REST Framework applications.',
    'long_description': None,
    'author': 'David Charboneau',
    'author_email': 'david@adadabase.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.6,<4.0.0',
}


setup(**setup_kwargs)
