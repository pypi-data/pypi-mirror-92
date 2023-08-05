# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_mat_report']

package_data = \
{'': ['*']}

entry_points = \
{u'pytest11': ['mat_report = pytest_mat_report.plugin']}

setup_kwargs = {
    'name': 'pytest-mat-report',
    'version': '0.0.0',
    'description': 'this is report',
    'long_description': None,
    'author': '\xe8\xa7\xa3\xe9\x87\x8a',
    'author_email': 'xieshi@forchange.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
