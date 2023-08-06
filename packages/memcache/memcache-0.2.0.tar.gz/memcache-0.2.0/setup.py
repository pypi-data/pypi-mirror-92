# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['memcache']
setup_kwargs = {
    'name': 'memcache',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'An Long',
    'author_email': 'aisk1988@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
