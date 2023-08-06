# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rdap']

package_data = \
{'': ['*']}

install_requires = \
['munge>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['rdap = rdap.cli:main']}

setup_kwargs = {
    'name': 'rdap',
    'version': '1.2.2',
    'description': 'Registration Data Access Protocol tools',
    'long_description': '\n# rdap\n\n[![PyPI](https://img.shields.io/pypi/v/rdap.svg?maxAge=3600)](https://pypi.python.org/pypi/rdap)\n[![PyPI](https://img.shields.io/pypi/pyversions/rdap.svg?maxAge=3600)](https://pypi.python.org/pypi/rdap)\n[![Tests](https://github.com/20c/rdap/workflows/tests/badge.svg)](https://github.com/20c/rdap)\n[![Codecov](https://img.shields.io/codecov/c/github/20c/rdap/master.svg?maxAge=3600)](https://codecov.io/github/20c/rdap)\n\nRegistration Data Access Protocol tools\n\n## Installation\n\n```sh\npip install rdap\n```\n\n\n## Usage\n\n```sh\nusage: rdap [-h] [--debug] [--home HOME] [--verbose] [--quiet] [--version] [--output-format OUTPUT_FORMAT] [--show-requests] [--parse]\n            [--write-bootstrap-data]\n            query [query ...]\n\nrdap\n\npositional arguments:\n  query\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --debug               enable extra debug output\n  --home HOME           specify the home directory, by default will check in order: $RDAP_HOME, ./.rdap, /home/$USER/.rdap,\n                        /home/$USER/.config/rdap\n  --verbose             enable more verbose output\n  --quiet               no output at all\n  --version             show version number and exit\n  --output-format OUTPUT_FORMAT\n                        output format (yaml, json, text)\n  --show-requests       show all requests\n  --parse               parse data into object before display\n  --write-bootstrap-data\n                        write bootstrap data for type (as query)\n```\n\n\n## Config file\n\nThe client uses the `--home` option to point to a directory, by default will check in order: `$RDAP_HOME`, `./.rdap`, `~/.rdap`, `~/.config/rdap`\n\nThe directory should have a `config.yaml` file in it, defaults shown below.\n\n```yaml\nrdap:\n  # URL to bootstrap the initial request off\n  bootstrap_url: https://rdap.db.ripe.net/\n  # boolean to use data from bootstrap_data_url instead of a bootstrap server\n  self_bootstrap: False\n  # url to load bootstrap data from\n  bootstrap_data_url: "https://data.iana.org/rdap/"\n  # length of time in hours to keep bootstrap data\n  bootstrap_cache_ttl: 25\n  # how to format the output\n  output_format: yaml\n  # API key for use at rdap.lacnic.net\n  lacnic_apikey: None\n  # role types to recursively query when processing\n  recurse_roles: ["administrative", "technical"]\n  # HTTP request timeout in seconds, used for both connect and read\n  timeout: 0.5\n```\n\n\n### License\n\nCopyright 2016 20C, LLC\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this softare except in compliance with the License.\nYou may obtain a copy of the License at\n\n   http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n',
    'author': '20C',
    'author_email': 'code@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/20c/rdap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
