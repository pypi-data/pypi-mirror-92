# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pydantic_settings']
install_requires = \
['Django>=3.1.5,<4.0.0',
 'dj-database-url>=0.5.0,<0.6.0',
 'pydantic>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'django-pydantic-settings',
    'version': '0.1.0',
    'description': 'Manage Django settings with Pydantic.',
    'long_description': '# django-pydantic-settings\n\n## Use pydantic settings management to simplify configuration of Django settings.\n\nVery much a work in progress, but reads the standard DJANGO_SETTINGS_MODULE environment variable (defaulting to pydantic_settings.Settings) to load a sub-class of pydantic_settings.Settings. All settings (that have been defined in pydantic_settings.Settings) can be overridden with environment variables. A special DatabaseSettings class is used to allow multiple databases to be configured simply with DSNs.\n\n## Database configuration\n\nBy defining multiple `DjangoDsn` attributes of the `DatabaseSettings` class, you can easily configure one or more database connections with environment variables. DSNs are parsed using dj-database-url.\n\n```python\nclass DatabaseSettings(BaseSettings):\n    default: DjangoDsn = Field(env="DATABASE_URL")\n    secondary: DjangoDsn = Field(env="SECONDARY_DATABASE_URL")\n```\n\n```python\n\xe2\x9d\xaf DATABASE_URL=sqlite:///foo SECONDARY_DATABASE_URL=sqlite:///bar ./settings_test/manage.py shell\nPython 3.9.1 (default, Jan  8 2021, 17:17:43)\n[Clang 12.0.0 (clang-1200.0.32.28)] on darwin\nType "help", "copyright", "credits" or "license" for more information.\n(InteractiveConsole)\n>>> from django.conf import settings\n...\n>>> pp.pprint(settings.DATABASES)\n{   \'default\': {   \'ATOMIC_REQUESTS\': False,\n                   \'AUTOCOMMIT\': True,\n                   \'CONN_MAX_AGE\': 0,\n                   \'ENGINE\': \'django.db.backends.sqlite3\',\n                   \'HOST\': \'\',\n                   \'NAME\': \'foo\',\n                   \'OPTIONS\': {},\n                   \'PASSWORD\': \'\',\n                   \'PORT\': \'\',\n                   \'TEST\': {   \'CHARSET\': None,\n                               \'COLLATION\': None,\n                               \'MIGRATE\': True,\n                               \'MIRROR\': None,\n                               \'NAME\': None},\n                   \'TIME_ZONE\': None,\n                   \'USER\': \'\'},\n    \'secondary\': {   \'CONN_MAX_AGE\': 0,\n                     \'ENGINE\': \'django.db.backends.sqlite3\',\n                     \'HOST\': \'\',\n                     \'NAME\': \'bar\',\n                     \'PASSWORD\': \'\',\n                     \'PORT\': \'\',\n                     \'USER\': \'\'}}\n>>>\n```\n',
    'author': 'Josh Ourisman',
    'author_email': 'me@josho.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joshourisman/django-pydantic-settings',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
