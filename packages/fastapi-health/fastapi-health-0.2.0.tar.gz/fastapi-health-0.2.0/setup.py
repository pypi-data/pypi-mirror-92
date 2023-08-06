# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_health']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0']

setup_kwargs = {
    'name': 'fastapi-health',
    'version': '0.2.0',
    'description': 'Heath check on FastAPI applications.',
    'long_description': '<h1 align="center">\n    <strong>fastapi-health</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/fastapi-health" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/fastapi-health" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/fastapi-health/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/fastapi-health">\n    <br />\n    <a href="https://pypi.org/project/fastapi-health" target="_blank">\n        <img src="https://img.shields.io/pypi/v/fastapi-health" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/fastapi-health">\n    <img src="https://img.shields.io/github/license/Kludex/fastapi-health">\n</p>\n\n\n## Installation\n\n``` bash\npip install fastapi-health\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/fastapi-health',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
