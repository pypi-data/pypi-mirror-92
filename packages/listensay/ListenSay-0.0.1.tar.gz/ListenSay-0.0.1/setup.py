# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['listensay']
setup_kwargs = {
    'name': 'listensay',
    'version': '0.0.1',
    'description': 'LS_Convert().say(text = "Hello, world!")',
    'long_description': None,
    'author': 'MadRock2',
    'author_email': 'MadRock2@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
