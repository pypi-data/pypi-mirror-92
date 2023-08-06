# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['valuesconverterprogram']
setup_kwargs = {
    'name': 'valuesconverterprogram',
    'version': '1.0.0',
    'description': 'This module is able to convert any values!!!',
    'long_description': None,
    'author': 'FlexonaFFt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
