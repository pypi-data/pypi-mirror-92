# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datalakebundle',
 'datalakebundle.hdfs',
 'datalakebundle.notebook',
 'datalakebundle.notebook.decorator',
 'datalakebundle.notebook.decorator.tests',
 'datalakebundle.table',
 'datalakebundle.table.config',
 'datalakebundle.table.create',
 'datalakebundle.table.delete',
 'datalakebundle.table.identifier',
 'datalakebundle.table.optimize',
 'datalakebundle.table.schema',
 'datalakebundle.test']

package_data = \
{'': ['*'], 'datalakebundle': ['_config/*']}

install_requires = \
['console-bundle>=0.3.1,<0.4.0',
 'databricks-bundle>=0.7.0a1',
 'injecta>=0.9.1,<0.10.0',
 'pyfony-bundles>=0.3.2,<0.4.0',
 'simpleeval>=0.9.10,<1.0.0']

entry_points = \
{'pyfony.bundle': ['create = datalakebundle.DataLakeBundle:DataLakeBundle']}

setup_kwargs = {
    'name': 'datalake-bundle',
    'version': '0.5.0a12',
    'description': 'DataLake tables management bundle for the Bricksflow Framework',
    'long_description': '# Datalake bundle\n\n![alt text](./docs/notebook-functions.png)\n\nThis bundle provides everything you need to create and manage a Databricks-based DataLake(House):\n\n* Tools to simplify & automate table creation, updates and migrations.\n* Explicit table schema enforcing for Hive tables, CSVs, ...\n* Decorators to write well-maintainable and self-documented function-based notebooks\n* Rich configuration options to customize naming standards, paths, and basically anything to match your needs\n\n## Installation\n\nInstall the bundle via Poetry:\n\n```\n$ poetry add datalake-bundle\n```\n\n## Usage\n\n1. [Recommended notebooks structure](docs/structure.md)\n1. [Defining DataLake tables](docs/tables.md)\n1. [Using datalake-specific notebook functions](docs/notebook-functions.md)\n1. [Using table-specific configuration](docs/configuration.md)\n1. [Tables management](docs/tables-management.md)\n1. [Parsing fields from table identifier](docs/parsing-fields.md)\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bricksflow/datalake-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
