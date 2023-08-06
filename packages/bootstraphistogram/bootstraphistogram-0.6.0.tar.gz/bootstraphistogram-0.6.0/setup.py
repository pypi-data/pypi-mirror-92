# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bootstraphistogram']

package_data = \
{'': ['*']}

install_requires = \
['boost-histogram>=0.7.0', 'matplotlib>=3.1,<4.0', 'numpy>=1.19.0,<2.0.0']

setup_kwargs = {
    'name': 'bootstraphistogram',
    'version': '0.6.0',
    'description': 'Poisson bootstrap histogram.',
    'long_description': '# bootstraphistogram \n\n[![Github Build Status](https://img.shields.io/github/workflow/status/davehadley/bootstraphistogram/ci?label=Github%20Build)](https://github.com/davehadley/bootstraphistogram/actions?query=workflow%3Aci)\n[![Documentation Status](https://readthedocs.org/projects/bootstraphistogram/badge/?version=latest)](https://bootstraphistogram.readthedocs.io/en/latest/?badge=latest)\n[![PyPI](https://img.shields.io/pypi/v/bootstraphistogram)](https://pypi.org/project/bootstraphistogram/)\n[![License: MIT](https://img.shields.io/pypi/l/bootstraphistogram)](https://github.com/davehadley/bootstraphistogram/blob/master/LICENSE.txt)\n[![Last Commit](https://img.shields.io/github/last-commit/davehadley/bootstraphistogram/dev)](https://github.com/davehadley/bootstraphistogram)\n\nA python package that provides a multi-dimensional histogram with automatic Poisson bootstrap re-sampling.\nSee the documentation at: <https://bootstraphistogram.readthedocs.io>.\n',
    'author': 'David Hadley',
    'author_email': 'davehadley@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/davehadley/bootstraphistogram',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
