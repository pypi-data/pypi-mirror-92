# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linesman']

package_data = \
{'': ['*']}

install_requires = \
['geographiclib>=1.50,<2.0', 'gpxpy>=1.4.2,<2.0.0', 'pyproj>=3.0.0,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['linesman = linesman:run']}

setup_kwargs = {
    'name': 'gpx-linesman',
    'version': '0.3.0',
    'description': 'Command line tool for measuring the straightness of a gpx track',
    'long_description': '# linesman\n[![test coverage](https://coveralls.io/repos/github/burrscurr/linesman/badge.svg)](https://coveralls.io/github/burrscurr/linesman)\n[![Documentation Status](https://readthedocs.org/projects/linesman/badge/?version=latest)](https://linesman.readthedocs.io/en/latest/?badge=latest)\n\n`linesman` is a small python command line tool calculating quality measures for\nthe straightness of a gpx track. The project is inspired by the "I attempted to\ncross \\<country\\> in a completely straight line" series of youtuber\n[GeoWizard](https://www.youtube.com/channel/UCW5OrUZ4SeUYkUg1XqcjFYA).\n\n## Installation\n\nAs a [python](https://python.org) package, `linesman` is installed [with\npip](https://datatofish.com/install-package-python-using-pip/). The\npackage is named `gpx-linesman`:\n\n```\npip install gpx-linesman\n```\n\nAfter installing the package, you should be able to run linesman:\n\n```\nlinesman --help\n```\n\n## Usage\n\n`linesman` must be passed a gpx file with the recorded track and a quality\nmeasure that shall be used to compare the gpx track against the reference line:\n\n```\nlinesman path/to/file.gpx <measure>\n```\n\nCurrently, the following quality measures are implemented:\n\n - `MAX`: maximum deviation from the reference line in meters\n - `AVG`: average deviation in meters\n - `SQ-AVG`: squared deviation average in meters\n\n## Development\n\nPython dependencies are managed with poetry and can be installed from\n`poetry.lock` by running:\n\n```\npoetry install\n```\n\nThen, the CLI tool can be started with `poetry run linesman`. Run tests with\n`poetry run pytest`.\n\n## Documentation\n\nConceptual documentation can be found on [readthedocs](https://linesman.readthedocs.io).\n',
    'author': 'burrscurr',
    'author_email': 'burrscurr@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/burrscurr/linesman.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
