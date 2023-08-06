# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dp2rathena']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'tortilla>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['dp2rathena = dp2rathena.cli:dp2rathena']}

setup_kwargs = {
    'name': 'dp2rathena',
    'version': '0.2.5',
    'description': 'Convert Divine-Pride API data to rAthena YAML',
    'long_description': "# dp2rathena: Divine-Pride API to rAthena\n\n[![PyPI - Version](https://img.shields.io/pypi/v/dp2rathena)](https://pypi.org/project/dp2rathena/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dp2rathena)](https://pypi.org/project/dp2rathena/)\n[![TravisCI Status](https://img.shields.io/travis/com/Latiosu/dp2rathena)](https://travis-ci.com/github/Latiosu/dp2rathena)\n[![codecov](https://codecov.io/gh/Latiosu/dp2rathena/branch/master/graph/badge.svg?token=B7G9O57UR8)](https://codecov.io/gh/Latiosu/dp2rathena)\n\nConvert Divine-Pride API data to rAthena DB formats (item_db.yml).\n\n## Requirements\n\n* Python 3.6+\n\n## Installation\n\n```\npip install dp2rathena\n```\n\n## Usage\n\nA [divine-pride.net](https://www.divine-pride.net/) API key is required, create an account and\ngenerate a key if you don't have one yet.\n\n```bash\ndp2rathena config\ndp2rathena item 501 1101\n```\n\n## Contributing\n\nThis project uses [poetry](https://python-poetry.org/) to manage the development enviroment.\n\n* Setup a local development environment with `poetry install`.\n* Run tests with `poetry run tox`\n* Execute script with `poetry run dp2rathena`\n\n## Changelog\n\nSee [CHANGELOG.md](https://github.com/Latiosu/dp2rathena/blob/master/CHANGELOG.md)\n\n## License\n\nSee [LICENSE](https://github.com/Latiosu/dp2rathena/blob/master/LICENSE)\n",
    'author': 'Eric Liu',
    'author_email': 'latiosworks@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Latiosu/dp2rathena',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
