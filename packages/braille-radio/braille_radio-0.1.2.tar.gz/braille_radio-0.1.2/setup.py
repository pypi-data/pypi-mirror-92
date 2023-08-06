# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['braille_radio']

package_data = \
{'': ['*']}

install_requires = \
['Whoosh>=2.7.4,<3.0.0',
 'addict>=2.4.0,<3.0.0',
 'progressbar>=2.5,<3.0',
 'python-vlc>=3.0.11115,<4.0.0']

entry_points = \
{'console_scripts': ['bradio = braille_radio.gui:main',
                     'braille_radio = braille_radio.gui:main']}

setup_kwargs = {
    'name': 'braille-radio',
    'version': '0.1.2',
    'description': 'A minimal internet radio optimized for braille users',
    'long_description': '# braille_radio\n\nA neat commandline internet radio for braille users or small character displays (e.g. Raspberry Pi).\n\n### Function\n\nBraille_radio plays internet radio stations. The station information is gathered from\nthe open radio data project [https://www.radio-browser.info](https://www.radio-browser.info).\n\n### Slow indexing for lighting fast searching:\n\nThe station information is processed by [Whoosh](https://whoosh.readthedocs.io/en/latest/intro.html) into a quick search index.\nTherefore the initial start of braille_radio will need a minute or two to create the index, so please be patient. \nThe subsequent starts will be quite fast. Then you can fluidly search (offline) as you type.\n\n### Optimized GUI:\n\nThe GUI is quite minimal. The main action takes place in the top line of the screen. This is for the comfort of the braille users. \nAdditional lines are displayed for further help/information, only.\n\n### Sound output:\n\nThe sound output is via VLC only. So you will need VLC to use this software.\n\n### Work in progress\n\nThis is a work in progress. Please open an issue if you have a question, found a bug or like to introduce some new ideas. \n\n### Installation:\n\n    $ pip install braille_radio\n    \n\n### Usage:\n\n    $ braille_radio\n    \n    or\n    \n    $ bradio\n    \n\n    \n\n\n\n\n\n\n',
    'author': 'volker',
    'author_email': 'volker.jaenisch@inqbus.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Inqbus/braille_radio.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
