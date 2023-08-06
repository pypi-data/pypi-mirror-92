# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brain_games', 'brain_games.games', 'brain_games.scripts']

package_data = \
{'': ['*']}

install_requires = \
['prompt>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['brain-even = brain_games.scripts.brain_even:main',
                     'brain-games = brain_games.scripts.brain_games:main']}

setup_kwargs = {
    'name': 'hexlet-code-nick',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Nikita',
    'author_email': 'Nick026rus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
