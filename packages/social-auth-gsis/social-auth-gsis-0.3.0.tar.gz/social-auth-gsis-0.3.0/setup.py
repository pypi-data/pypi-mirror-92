# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['social_auth_gsis']
install_requires = \
['django>=2.2.0',
 'social-auth-app-django>=4.0.0,<5.0.0',
 'social-auth-core>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'social-auth-gsis',
    'version': '0.3.0',
    'description': 'Social Auth backend for Greek GSIS',
    'long_description': None,
    'author': 'Paris Kasidiaris',
    'author_email': 'paris@sourcelair.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
