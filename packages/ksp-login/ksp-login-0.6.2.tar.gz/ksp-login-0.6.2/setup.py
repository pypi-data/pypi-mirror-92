# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ksp_login', 'ksp_login.templatetags']

package_data = \
{'': ['*'],
 'ksp_login': ['locale/sk/LC_MESSAGES/*',
               'static/ksp_login/css/*',
               'static/ksp_login/img/*',
               'static/ksp_login/js/*',
               'templates/ksp_login/*',
               'templates/ksp_login/parts/*']}

install_requires = \
['django>=1.11', 'social-auth-app-django>=3.1', 'social-auth-core>=3.0']

setup_kwargs = {
    'name': 'ksp-login',
    'version': '0.6.2',
    'description': 'KSP Login is an app for easy authentication management with support for',
    'long_description': None,
    'author': 'Michal Petrucha',
    'author_email': 'michal.petrucha@koniiiik.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
