# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['klickbrick_mb']
entry_points = \
{'console_scripts': ['klickbrick = entry:main']}

setup_kwargs = {
    'name': 'klickbrick-mb',
    'version': '0.1.0',
    'description': 'An Extensible Python CLI',
    'long_description': None,
    'author': 'Matthias Busch',
    'author_email': 'dev.mbusch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
