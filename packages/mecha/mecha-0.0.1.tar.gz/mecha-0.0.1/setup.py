# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mecha']

package_data = \
{'': ['*']}

install_requires = \
['beet>=0.5.1,<0.6.0']

setup_kwargs = {
    'name': 'mecha',
    'version': '0.0.1',
    'description': 'A bulletproof Minecraft command generation library',
    'long_description': '# Mecha\n\n[![GitHub Actions](https://github.com/vberlier/mecha/workflows/CI/badge.svg)](https://github.com/vberlier/mecha/actions)\n[![PyPI](https://img.shields.io/pypi/v/mecha.svg)](https://pypi.org/project/mecha/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mecha.svg)](https://pypi.org/project/mecha/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n> A bulletproof Minecraft command generation library.\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\n$ pip install mecha\n```\n\n---\n\nLicense - [MIT](https://github.com/vberlier/mecha/blob/main/LICENSE)\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vberlier/mecha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
