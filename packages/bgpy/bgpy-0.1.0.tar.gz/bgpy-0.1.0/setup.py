# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bgpy', 'bgpy.example']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['bgpy = bgpy.cli:main']}

setup_kwargs = {
    'name': 'bgpy',
    'version': '0.1.0',
    'description': 'Running local or remote python servers in the background and establish stream socket-based communication with clients.',
    'long_description': '\n====\nbgpy\n====\n\n.. image:: https://img.shields.io/pypi/v/bgpy.svg\n        :target: https://pypi.python.org/pypi/bgpy\n\n.. image:: https://github.com/munterfinger/bgpy/workflows/check/badge.svg\n        :target: https://github.com/munterfinger/bgpy/actions?query=workflow%3Acheck\n\n.. image:: https://readthedocs.org/projects/bgpy/badge/?version=latest\n        :target: https://bgpy.readthedocs.io/en/latest/\n        :alt: Documentation Status\n\n.. image:: https://codecov.io/gh/munterfinger/bgpy/branch/master/graph/badge.svg\n        :target: https://codecov.io/gh/munterfinger/bgpy\n\nRunning local or remote python servers in the background using :code:`Popen` from the\nsubprocess module and establish stream socket-based communication with clients\nin both directions.\n\nGetting started\n---------------\n\nGet the stable release of the package from pypi:\n\n.. code-block:: shell\n\n    pip install bgpy\n\n\nRun an example background process on localhost and communicate using stream sockets:\n\n.. code-block:: python\n\n    from bgpy.interface import initialize, execute, terminate\n    from bgpy.example.tasks import init_task, exec_task, exit_task\n\n    # Start background process\n    initialize(init_task, exec_task, exit_task)\n\n    # Increase value\n    execute({"command": "increase", "value_change": 10})\n\n    # Decrease value\n    execute({"command": "decrease", "value_change": 100})\n\n    # Terminate\n    args = terminate(await_response=True)\n\nLicense\n-------\n\nThis project is licensed under the MIT License - see the LICENSE file for details',
    'author': 'Merlin Unterfinger',
    'author_email': 'info@munterfinger.ch',
    'maintainer': 'Merlin Unterfinger',
    'maintainer_email': 'info@munterfinger.ch',
    'url': 'https://pypi.org/project/bgpy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
