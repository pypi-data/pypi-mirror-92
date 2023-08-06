# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gapi_helper',
 'gapi_helper.drive',
 'gapi_helper.mail',
 'gapi_helper.sheets',
 'gapi_helper.tasks']

package_data = \
{'': ['*']}

install_requires = \
['Flask-SQLAlchemy>=2.4.4,<3.0.0',
 'Flask>=1.1.2,<2.0.0',
 'google-api-python-client>=1.12.8,<2.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'simpletasks-data>=0.1.0,<0.2.0',
 'simpletasks>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'gapi-helper',
    'version': '0.1.0',
    'description': 'Helpers around Google APIs',
    'long_description': '# gapi-helper\n\nHelpers around Google APIs\n\n\n----\nContributing\n\n```\npoetry install --no-root\n```',
    'author': 'Thomas Muguet',
    'author_email': 'thomas.muguet@upowa.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/upOwa/gapi-helper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
