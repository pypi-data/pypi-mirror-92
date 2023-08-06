# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jara_utils', 'jara_utils.decorators', 'jara_utils.normalization']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2020.1,<2021.0']

extras_require = \
{'test': ['pytest>=6.1.2,<7.0.0',
          'Faker>=4.14.0,<5.0.0',
          'pytest-sugar>=0.9.4,<0.10.0',
          'flake8>=3.8.4,<4.0.0',
          'pytest-cov>=2.10.1,<3.0.0',
          'mypy>=0.790,<0.791',
          'flake8-quotes>=3.2.0,<4.0.0',
          'pytest-asyncio>=0.14.0,<0.15.0',
          'flake8-pytest-style>=1.3.0,<2.0.0',
          'flake8-comprehensions>=3.3.1,<4.0.0',
          'flake8-multiline-containers>=0.0.17,<0.0.18',
          'flake8-builtins>=1.5.3,<2.0.0',
          'flake8-print>=4.0.0,<5.0.0',
          'flake8-debugger>=4.0.0,<5.0.0',
          'flake8-simplify>=0.12.0,<0.13.0',
          'flake8-annotations>=2.5.0,<3.0.0',
          'pytest-deadfixtures>=2.2.1,<3.0.0',
          'bandit>=1.7.0,<2.0.0']}

setup_kwargs = {
    'name': 'jara-utils',
    'version': '0.1.5',
    'description': 'A package with basic stuff.',
    'long_description': '=================\nJara core package\n=================\n\n    Jara means bear in `Sesotho`_.\n\n.. image:: https://img.shields.io/badge/python-3.7.x-blue.svg\n    :alt: Python 3.7.x\n\n.. image:: https://img.shields.io/badge/code_style-flake8-brightgreen.svg\n    :alt: Flake8\n\n.. image:: https://img.shields.io/badge/dependency_manager-poetry-blueviolet.svg\n    :alt: Poetry\n\nWhy?\n~~~~\nSometimes I start a new project and I need to implement again same methods and after create tests for each method. This package will provide common methods like ``str_2_bool`` or other methods check ``README.rst`` for all methods available.\n\nHow to contribute to the package?\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nClone project locally and then:\n\n* Install all dependencies including the test ones: ``poetry install -E test``;\n* Do changes in the project;\n* Create unittests (please make sure  you will keep coverage to 100%);\n* Run all sanity commands (pytest, flake8, mypy)\n\nNote: Run commands using poetry: ``poetry run pytest``;\n\nWhat you will find in this package?\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nBasically will contain utils methods to avoid write them in all projects. Some examples:\n\n* decorator to benchmark methods;\n* methods to handle environment variables;\n* some utils methods such as: ``snake_2_camel``, ``str_2_bool``.\n\n\n.. _Sesotho: https://en.wikipedia.org/wiki/Sotho_language\n',
    'author': 'Serban Senciuc',
    'author_email': 'senciuc.serban@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/senciucserban/jara-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
