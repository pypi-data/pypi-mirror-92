# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aoe2netwrapper', 'aoe2netwrapper.models']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0', 'pydantic>=1.7.3,<2.0.0', 'requests>=2.25.1,<3.0.0']

extras_require = \
{'dataframe': ['pandas>=1.0,<2.0'], 'docs': ['portray>=1.4.0,<2.0.0']}

setup_kwargs = {
    'name': 'aoe2netwrapper',
    'version': '0.3.1',
    'description': 'My Python wrapper for the aoe2.net data API',
    'long_description': '<h1 align="center">\n  <b>aoe2netwrapper</b>\n</h1>\n\n<p align="center">\n  <!-- PyPi Version -->\n  <a href="https://pypi.org/project/aoe2netwrapper">\n    <img alt="PyPI Version" src="https://img.shields.io/pypi/v/aoe2netwrapper?label=PyPI&logo=PyPI">\n  </a>\n\n  <!-- Github Release -->\n  <a href="https://github.com/fsoubelet/AoE2NetAPIWrapper/releases">\n    <img alt="Github Release" src="https://img.shields.io/github/v/release/fsoubelet/AoE2NetAPIWrapper?color=orange&label=Release&logo=Github">\n  </a>\n\n  <br/>\n\n  <!-- Github Actions Build -->\n  <a href="https://github.com/fsoubelet/AoE2NetAPIWrapper/actions?query=workflow%3A%22Tests%22">\n    <img alt="Github Actions" src="https://github.com/fsoubelet/AoE2NetAPIWrapper/workflows/Tests/badge.svg?branch=master">\n  </a>\n\n  <!-- Code Coverage -->\n  <a href="https://codeclimate.com/github/fsoubelet/AoE2NetAPIWrapper/maintainability">\n    <img alt="Code Coverage" src="https://img.shields.io/codeclimate/maintainability/fsoubelet/AoE2NetAPIWrapper?label=Maintainability&logo=Code%20Climate">\n  </a>\n\n  <br/>\n\n  <!-- Code style -->\n  <a href="https://github.com/psf/Black">\n    <img alt="Code Style" src="https://img.shields.io/badge/Code%20Style-Black-9cf.svg">\n  </a>\n\n  <!-- Linter -->\n  <a href="https://github.com/PyCQA/pylint">\n    <img alt="Linter" src="https://img.shields.io/badge/Linter-Pylint-ce963f.svg">\n  </a>\n\n  <!-- Build tool -->\n  <a href="https://github.com/python-poetry/poetry">\n    <img alt="Build tool" src="https://img.shields.io/badge/Build%20Tool-Poetry-4e5dc8.svg">\n  </a>\n\n  <!-- Test runner -->\n  <a href="https://github.com/pytest-dev/pytest">\n    <img alt="Test runner" src="https://img.shields.io/badge/Test%20Runner-Pytest-ce963f.svg">\n  </a>\n\n  <!-- License -->\n  <a href="https://github.com/fsoubelet/AoE2NetAPIWrapper/blob/master/LICENSE">\n    <img alt="License" src="https://img.shields.io/github/license/fsoubelet/AoE2NetAPIWrapper?color=9cf&label=License">\n  </a>\n</p>\n\n<p align="center">\n  A simple, efficient and typed wrapper to query the https://aoe2.net APIs with Python 3.6.1+\n</p>\n\n<p align="center">\n  <a href="https://www.python.org/">\n    <img alt="Made With Python" src="https://forthebadge.com/images/badges/made-with-python.svg">\n  </a>\n</p>\n\nLink to [documentation][package_doc].\n\nLink to [source code][package_source].\n\n## License\n\nCopyright &copy; 2021 Felix Soubelet. [MIT License](LICENSE)\n\n[package_doc]: https://fsoubelet.github.io/AoE2NetAPIWrapper/\n[package_source]: https://github.com/fsoubelet/AoE2NetAPIWrapper\n',
    'author': 'Felix Soubelet',
    'author_email': 'felix.soubelet@liverpool.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fsoubelet/AoE2NetAPIWrapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
