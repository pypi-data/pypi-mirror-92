# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['superinactive']

package_data = \
{'': ['*']}

install_requires = \
['supervisor>=4.2.1,<5.0.0']

entry_points = \
{'console_scripts': ['superinactive = superinactive.superinactive:main',
                     'touch_file = superinactive.touch_file:main']}

setup_kwargs = {
    'name': 'superinactive',
    'version': '0.1.0',
    'description': '',
    'long_description': '# superinactive\nSupervisor plugin to monitor for file activity and restart program on inactivity\n\nImagine you have an infinite long running `ffmpeg` job, which converts a video stream on the fly.\nAfter a certain time the file output does not change any more but supervisor does not detect the `ffmpeg` job as crashed.\n\nThis plugin may solve such situations.  \n\nInstallation:\n\n    pip3 install superinactive\n\nConfiguration:\n\n    [program:ffmpeg]\n    command=ffmpeg ......  -o /home/volker/out.stream\n\n    [program:superinactive]\n    command=superinactive /home/volker/out.stream 10 ffmpeg\n\nCommand line options:\n\n    usage: superinactive.py [-h] [-g GROUP] [-a] path timeout [prog [prog ...]]\n\n    Supervisor plugin to monitor a file activity and restart programs on\n    inactivity\n\n    optional arguments:\n      -h, --help            show this help message and exit\n\n    file monitoring:\n      path                  file path to monitor for inactivity\n      timeout               timeout (seconds) for inactivity\n\n    programs:\n      prog                  supervisor program name to restart\n      -g GROUP, --group GROUP\n                            supervisor group name to restart\n      -a, --any             restart any child of this supervisor\n',
    'author': 'volker',
    'author_email': 'volker.jaenisch@inqbus.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Inqbus/superinactive.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
