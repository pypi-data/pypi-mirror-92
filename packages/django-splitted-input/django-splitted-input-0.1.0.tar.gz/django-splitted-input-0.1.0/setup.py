# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_splitted_input']

package_data = \
{'': ['*'],
 'django_splitted_input': ['static/django_splitted_input/css/*',
                           'static/django_splitted_input/js/*',
                           'templates/django_splitted_input/*']}

install_requires = \
['Django>=3.1.5,<4.0.0']

setup_kwargs = {
    'name': 'django-splitted-input',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Julian Leucker',
    'author_email': 'leuckerj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)
