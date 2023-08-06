# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_swagger_tester', 'django_swagger_tester.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0', 'djangorestframework']

setup_kwargs = {
    'name': 'django-swagger-tester',
    'version': '2.2.1',
    'description': 'Django test utility for validating Swagger documentation',
    'long_description': 'Django Swagger Tester has been renamed to ``drf-openapi-tester``.\n\nPlease migrate for updates.\n\nGithub: https://github.com/snok/drf-openapi-tester\n\nPyPi: https://pypi.org/project/drf-openapi-tester',
    'author': 'Sondre Lillebø Gundersen',
    'author_email': 'sondrelg@live.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/snok/django-swagger-tester',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
