# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polybar_clockify']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.7.3,<4.0.0',
 'dataclasses-json>=0.5.2,<0.6.0',
 'isodate>=0.6.0,<0.7.0',
 'marshmallow>=3.10.0,<4.0.0',
 'pytz>=2020.5,<2021.0',
 'websockets>=8.1,<9.0']

entry_points = \
{'console_scripts': ['polybar-clockify = polybar_clockify.app:run']}

setup_kwargs = {
    'name': 'polybar-clockify',
    'version': '0.2.8',
    'description': 'Control Clockify through Polybar',
    'long_description': '.. image:: https://badge.fury.io/py/polybar-clockify.svg\n    :target: https://badge.fury.io/py/polybar-clockify\n\n================\npolybar-clockify\n================\n.. image:: https://raw.githubusercontent.com/woutdp/polybar-clockify/master/demo/demo.gif\n.. contents::\n\nIntroduction\n------------\n\nControl Clockify through Polybar.\n\n\nFeatures:\n\n- Displaying money earned and time worked\n- Toggle timer\n- Daily, weekly and monthly view\n- Hide output for privacy\n\n\nInstallation\n------------\n::\n\n    pip install polybar-clockify\n\n\nConfiguration\n_____________\nCreate credentials file in ``~/.config/polybar/clockify/credentials.json`` and fill out your clockify credentials.\nYou will have to create a `clockify API key <https://clockify.me/user/settings/>`_ to make the module work. ::\n\n    {\n      "api-key": "your-api-key",\n      "email": "your-email",\n      "password": "your-password"\n    }\n\n\nCreate a polybar module inside your polybar config add it to your active modules. ::\n\n    [module/clockify]\n    type = custom/script\n    tail = true\n    exec = polybar-clockify\n    click-left = echo \'TOGGLE_TIMER\' | nc 127.0.0.1 30300\n    click-right = echo \'TOGGLE_HIDE\' | nc 127.0.0.1 30300\n    scroll-up = echo \'NEXT_MODE\' | nc 127.0.0.1 30300\n    scroll-down = echo \'PREVIOUS_MODE\' | nc 127.0.0.1 30300\n\n\nDevelopment\n-----------\nThis package uses `poetry <https://python-poetry.org/>`_\n\nTo run in the terminal ::\n\n    # Execute in the root folder of the repository\n    poetry run python -u ./polybar_clockify/app.py\n\n    # Example for polybar config\n    [module/clockify]\n    type = custom/script\n    tail = true\n    exec = poetry run python -u /home/<your_user>/polybar-clockify/polybar_clockify/app.py\n\n\nContribution\n____________\nAt the moment the functionality is pretty basic, but sufficient for my use case.\nIf you want to extend the functionality I\'d be delighted to accept pull requests!',
    'author': 'Wout De Puysseleir',
    'author_email': 'woutdp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/woutdp/polybar-clockify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
