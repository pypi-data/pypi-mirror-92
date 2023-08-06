# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cruft_helloworld', 'cruft_helloworld.services', 'cruft_helloworld.tools']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.21,<0.30.0',
 'click-default-group>=1.2.2,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'colorlog>=4.6.2,<5.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'python-geoip-geolite2>=2015.0303,<2016.0',
 'python-geoip-python3>=1.3,<2.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.4.0,<10.0.0']

entry_points = \
{'console_scripts': ['helloworld = cruft_helloworld.app:cli']}

setup_kwargs = {
    'name': 'cruft-helloworld',
    'version': '0.4.2',
    'description': 'Cruft Python Hello-World',
    'long_description': '# cruft_helloworld\n\n![PyPI](https://img.shields.io/pypi/v/cruft_helloworld?style=flat-square)\n![GitHub Workflow Status (master)](https://img.shields.io/github/workflow/status/yoyonel/cruft_helloworld/Test%20&%20Lint/master?style=flat-square)\n![Coveralls github branch](https://img.shields.io/coveralls/github/yoyonel/cruft_helloworld/master?style=flat-square)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cruft_helloworld?style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/cruft_helloworld?style=flat-square)\n\nCruft Python Hello-World\n\n## Requirements\n\n* Python 3.7.3 or newer\n* [poetry](https://poetry.eustance.io/) 1.1 or newer\n\n## Installation\n\n```sh\npip install cruft_helloworld\n```\n\n## Development\n\nThis project uses [poetry](https://poetry.eustace.io/) for packaging and\nmanaging all dependencies and [pre-commit](https://pre-commit.com/) to run\n[flake8](http://flake8.pycqa.org/), [isort](https://pycqa.github.io/isort/),\n[mypy](http://mypy-lang.org/) and [black](https://github.com/python/black).\n\nClone this repository and run\n\n```bash\npoetry install\npoetry run pre-commit install\n```\n\nto create a virtual environment containing all dependencies.\nAfterwards, You can run the test suite using\n\n```bash\npoetry run pytest\n```\n\nThis repository follows the [Conventional Commits](https://www.conventionalcommits.org/)\nstyle.\n\n### Pycharm debugging\n[Debuggers and PyCharm](https://pytest-cov.readthedocs.io/en/latest/debuggers.html)\n> Coverage does not play well with other tracers simultaneously running.\n> This manifests itself in behaviour that PyCharm might not hit a breakpoint no matter what the user does.\n\n### Cookiecutter template\n\nThis project was created using [cruft](https://github.com/cruft/cruft) and the\n[cookiecutter-pyproject](https://github.com/escaped/cookiecutter-pypackage) template.\nIn order to update this repository to the latest template version run\n\n```sh\ncruft update\n```\n\nin the root of this repository.\n',
    'author': 'lionel atty',
    'author_email': 'yoyonel@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yoyonel/cruft_helloworld',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.9,<4.0',
}


setup(**setup_kwargs)
