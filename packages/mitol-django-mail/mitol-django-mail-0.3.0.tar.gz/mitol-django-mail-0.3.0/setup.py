# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mitol', 'mitol.mail']

package_data = \
{'': ['*'], 'mitol.mail': ['templates/mail/*', 'templates/mail/partials/*']}

install_requires = \
['Django>=2.2.12,<3.2',
 'beautifulsoup4>=4.6.0,<5.0.0',
 'django-anymail>=6.1,<9.0',
 'html5lib>=1.1,<2.0',
 'mitol-django-common>=0.4.0,<0.5.0',
 'premailer>=3.7.0,<4.0.0',
 'toolz>=0.9,<0.10']

extras_require = \
{'dev': ['ipython>=7.13.0,<8.0.0'],
 'test': ['pytest>=6.0.2,<7.0.0',
          'pytest-cov',
          'pytest-mock==1.10.1',
          'pytest-django==3.10.0',
          'isort>=4.3.21,<5.0.0',
          'black>=19.10b0,<20.0',
          'pylint>=2.0,<3.0',
          'pylint-django>=2.0.2,<3.0.0',
          'mypy>=0.782,<0.783',
          'django-stubs==1.6.0']}

setup_kwargs = {
    'name': 'mitol-django-mail',
    'version': '0.3.0',
    'description': 'MIT Open Learning django app extensions for mail',
    'long_description': None,
    'author': 'MIT Office of Open Learning',
    'author_email': 'mitx-devops@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
