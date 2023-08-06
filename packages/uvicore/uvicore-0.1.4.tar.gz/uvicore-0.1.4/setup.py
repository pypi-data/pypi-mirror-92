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
['aiofiles>=0.5.0,<0.6.0',
 'alembic>=1.4.2,<2.0.0',
 'asyncclick>=7.0.9,<8.0.0',
 'colored>=1.4.2,<2.0.0',
 'databases>=0.3.2,<0.4.0',
 'environs>=8.0.0,<9.0.0',
 'fastapi>=0.61.1,<0.62.0',
 'gunicorn>=20.0.4,<21.0.0',
 'ipython>=7.18.1,<8.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'prettyprinter>=0.18.0,<0.19.0',
 'rx>=3.1.1,<4.0.0',
 'uvicorn>=0.11.8,<0.12.0']

setup_kwargs = {
    'name': 'uvicore',
    'version': '0.1.4',
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
