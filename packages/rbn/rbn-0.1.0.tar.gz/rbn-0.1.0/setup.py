# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rbn']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0', 'rich>=9.9.0,<10.0.0', 'telnetlib3>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'rbn',
    'version': '0.1.0',
    'description': 'A Python library for consuming data from the Reverse Beacon Network in real time',
    'long_description': '# Reverse Beacon Network client for Python\n\nThis is both a library and cli tool, under the package `rbn`\n\n## Installation\n\npyRBN can be installed from PYPI:\n\n```sh\npython3 -m pip install rbn\n```\n\nand imported as:\n\n```python\nimport rbn\n```\n\n## CLI Usage\n\n```text\nusage: rbn [-h] -c CALLSIGN [-b {630m,160m,80m,60m,40m,30m,20m,17m,15m,12m,10m,6m,4m,2m}] [-m {cw,rtty,psk31,psk63,ft8,ft4}] [-f FILTER_CALL]\n\nCLI frontend to the Reverse Beacon Network\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -c CALLSIGN, --callsign CALLSIGN\n                        Your callsign\n  -b {630m,160m,80m,60m,40m,30m,20m,17m,15m,12m,10m,6m,4m,2m}, --band {630m,160m,80m,60m,40m,30m,20m,17m,15m,12m,10m,6m,4m,2m}\n                        Band to filter by (this can be passed multiple times)\n  -m {cw,rtty,psk31,psk63,ft8,ft4}, --mode {cw,rtty,psk31,psk63,ft8,ft4}\n                        Mode to filter by (this can be passed multiple times)\n  -f FILTER_CALL, --filter-call FILTER_CALL\n                        Callign to filter by (this can be passed multiple times)\n```\n\n## Example library usage\n\nThe [`__main__.py`](https://github.com/Ewpratten/pyRBN/blob/master/rbn/__main__.py) file is kept fairly simple as an example of using this library.\n',
    'author': 'Evan Pratten',
    'author_email': 'ewpratten@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
