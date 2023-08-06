# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ctl', 'ctl.config', 'ctl.plugins', 'ctl.util']

package_data = \
{'': ['*'],
 'ctl': ['bin/ctl_venv_build',
         'bin/ctl_venv_build',
         'bin/ctl_venv_build',
         'bin/ctl_venv_copy',
         'bin/ctl_venv_copy',
         'bin/ctl_venv_copy',
         'bin/ctl_venv_sync',
         'bin/ctl_venv_sync',
         'bin/ctl_venv_sync']}

install_requires = \
['confu>=1.4,<2.0',
 'git-url-parse>=1.1,<2.0',
 'grainy>=1.4,<2.0',
 'munge>=1,<2',
 'pluginmgr>=1,<2']

entry_points = \
{'console_scripts': ['ctl = ctl.cli:main']}

setup_kwargs = {
    'name': 'ctl',
    'version': '0.3.1.1',
    'description': 'Full control of your environment',
    'long_description': None,
    'author': '20C',
    'author_email': 'code@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/20c/ctl',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
