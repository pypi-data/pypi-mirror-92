# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uvicore',
 'uvicore.auth',
 'uvicore.auth.commands',
 'uvicore.auth.config',
 'uvicore.auth.contractsOLD',
 'uvicore.auth.database.seeders',
 'uvicore.auth.database.tables',
 'uvicore.auth.models',
 'uvicore.configuration',
 'uvicore.configuration.commands',
 'uvicore.console',
 'uvicore.console.commands',
 'uvicore.console.commands.stubs',
 'uvicore.container',
 'uvicore.container.commands',
 'uvicore.contracts',
 'uvicore.database',
 'uvicore.database.OBSOLETE',
 'uvicore.database.commands',
 'uvicore.database.commands.stubs',
 'uvicore.events',
 'uvicore.events.commands',
 'uvicore.factories',
 'uvicore.foundation',
 'uvicore.foundation.config',
 'uvicore.foundation.decorators',
 'uvicore.http',
 'uvicore.http.OBSOLETE',
 'uvicore.http.OBSOLETE.controllers',
 'uvicore.http.commands',
 'uvicore.http.routing',
 'uvicore.http.templating',
 'uvicore.logging',
 'uvicore.orm',
 'uvicore.orm.commands',
 'uvicore.orm.commands.stubs',
 'uvicore.package',
 'uvicore.package.commands',
 'uvicore.support',
 'uvicore.typing']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'aiofiles>=0.6.0,<0.7.0',
 'alembic>=1.5.2,<2.0.0',
 'asyncclick>=7.1.2,<8.0.0',
 'colored>=1.4.2,<2.0.0',
 'databases>=0.4.1,<0.5.0',
 'environs>=9.3.0,<10.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'gunicorn>=20.0.4,<21.0.0',
 'ipython>=7.19.0,<8.0.0',
 'prettyprinter>=0.18.0,<0.19.0',
 'requests>=2.25.1,<3.0.0',
 'uvicorn>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'uvicore',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Matthew Reschke',
    'author_email': 'mail@mreschke.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
