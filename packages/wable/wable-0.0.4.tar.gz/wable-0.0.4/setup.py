# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['wable']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'wable',
    'version': '0.0.4',
    'description': 'A client to communicate with wable.org api',
    'long_description': '## Wable client\n\nA client to communicate with wable.org api.\n\n## Requirements\n\n- [python > 3.7](https://www.python.org/downloads/release/python-370/)\n- [pip](https://pip.pypa.io/en/stable/)\n\n## Development\n\nClone the repository\n\n```sh\npip install poetry\npoetry install\n```\n\nTo install a new python package\n\n```sh\npoetry add [NEW_PACKAGE]\n```\n\nTo export poetry lock file to `requirements.txt` run\n\n```sh\nmake deps\n```\n\n## Tests\n\n```sh\nmake test\n```\n\n## Installation\n\nThe package is published at https://pypi.org/project/wable/\n\n```sh\npip install wable\n```\n\n## Usage\n\n```python\nfrom wable.client import Wable\n\nw = Wable()\n# more to come here\n```\n',
    'author': 'Madhu',
    'author_email': 'madhu@wable.org',
    'maintainer': 'Madhu',
    'maintainer_email': 'madhu@wable.org',
    'url': 'https://wable.org',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.6',
}


setup(**setup_kwargs)
