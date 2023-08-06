# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lisa']
install_requires = \
['pytest-playbook>=0.1.0,<0.2.0',
 'pytest-xdist>=2.1.0,<3.0.0',
 'pytest>=6.1.2,<7.0.0',
 'schema==0.7.2']

entry_points = \
{'console_scripts': ['lisa = lisa:main'], 'pytest11': ['lisa = lisa']}

setup_kwargs = {
    'name': 'pytest-lisa',
    'version': '0.1.0',
    'description': 'Pytest plugin for organizing tests.',
    'long_description': '# pytest-lisa\n\nPytest plugin for organizing tests. Supports the LISAv3 framework.\n\nSee the [documentation][] for more information, and the LISAv3 [`README.md`][]\nfor notices.\n\n[documentation]: https://microsoft.github.io/lisa/modules/lisa.html\n[`README.md`]: https://github.com/microsoft/lisa/blob/andschwa/pytest/README.md\n',
    'author': 'Andrew Schwartzmeyer',
    'author_email': 'andrew@schwartzmeyer.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://microsoft.github.io/lisa',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
