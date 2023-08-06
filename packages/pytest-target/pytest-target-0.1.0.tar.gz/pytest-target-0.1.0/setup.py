# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['target']

package_data = \
{'': ['*']}

install_requires = \
['fabric>=2.5.0,<3.0.0',
 'filelock>=3.0.12,<4.0.0',
 'invoke>=1.4.1,<2.0.0',
 'pytest-playbook>=0.1.0,<0.2.0',
 'pytest>=6.1.2,<7.0.0',
 'tenacity>=6.2.0,<7.0.0']

entry_points = \
{'pytest11': ['target = target.plugin']}

setup_kwargs = {
    'name': 'pytest-target',
    'version': '0.1.0',
    'description': 'Pytest plugin for remote target orchestration.',
    'long_description': '# pytest-target\n\nPytest plugin for remote target orchestration. Supports the LISAv3 framework.\n\nSee the [documentation][] for more information, and the LISAv3 [`README.md`][]\nfor notices.\n\n[documentation]: https://microsoft.github.io/lisa/modules/target.html\n[`README.md`]: https://github.com/microsoft/lisa/blob/andschwa/pytest/README.md\n',
    'author': 'Andrew Schwartzmeyer',
    'author_email': 'andrew@schwartzmeyer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://microsoft.github.io/lisa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
