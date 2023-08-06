# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['playbook']
install_requires = \
['PyYAML>=5.3.1,<6.0.0', 'pytest>=6.1.2,<7.0.0', 'schema==0.7.2']

entry_points = \
{'pytest11': ['playbook = playbook']}

setup_kwargs = {
    'name': 'pytest-playbook',
    'version': '0.1.1',
    'description': 'Pytest plugin for reading playbooks.',
    'long_description': '# pytest-playbook\n\nPytest plugin for reading playbooks. Supports the LISAv3 framework.\n\nSee the [documentation][] for more information, and the LISAv3 [`README.md`][]\nfor notices.\n\n[documentation]: https://microsoft.github.io/lisa/modules/playbook.html\n[`README.md`]: https://github.com/microsoft/lisa/blob/andschwa/pytest/README.md\n',
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
