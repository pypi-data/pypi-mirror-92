# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['databricksbundle',
 'databricksbundle.bootstrap',
 'databricksbundle.dbutils',
 'databricksbundle.jdbc',
 'databricksbundle.notebook',
 'databricksbundle.notebook.decorator',
 'databricksbundle.notebook.decorator.tests',
 'databricksbundle.notebook.function',
 'databricksbundle.notebook.logger',
 'databricksbundle.notebook.path',
 'databricksbundle.spark',
 'databricksbundle.spark.config']

package_data = \
{'': ['*'], 'databricksbundle': ['_config/*', '_config/databricks/*']}

install_requires = \
['console-bundle>=0.3.1,<0.4.0',
 'injecta>=0.9.1,<0.10.0',
 'logger-bundle>=0.6.1,<0.7.0',
 'pyfony-bundles>=0.3.2,<0.4.0',
 'pyfony-core>=0.7.1,<0.8.0']

entry_points = \
{'pyfony.bundle': ['create = '
                   'databricksbundle.DatabricksBundle:DatabricksBundle.autodetect']}

setup_kwargs = {
    'name': 'databricks-bundle',
    'version': '0.7.0a1',
    'description': 'Databricks bundle for the Pyfony framework',
    'long_description': '# Databricks bundle\n\nThis bundle allows you to write **beautiful function-based notebooks**.\n\n![alt text](./docs/notebookFunction.png "Databricks function-based notebook example")\n\nCompared to bare notebooks, the function-based approach brings the **following advantages**: \n\n* create and publish auto-generated documentation and lineage of notebooks and pipelines (Bricksflow PRO) \n* write much cleaner notebooks with properly named code blocks\n* (unit)test specific notebook functions with ease\n* use YAML to configure your notebooks for given environment (dev/test/prod/...)\n* utilize pre-configured objects to automate repetitive tasks\n\nFunction-based notebooks have been designed to provide the same user-experience as bare notebooks.\nJust write the function, annotate it with the `@notebookFunction` decorator and run the cell.\n\nThis bundle is the main part of the [Bricksflow framework](https://github.com/bricksflow/bricksflow).\n\n## Installation\n\nInstall the bundle via Poetry:\n\n```\n$ poetry add databricks-bundle && poetry add databricks-connect --dev\n```\n\n## Usage\n\n1. [Using pre-configured objects](docs/dependencies.md)\n1. [Configuring notebook functions](docs/configuration.md)\n1. [Databricks Connect setup](docs/databricks-connect.md)\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bricksflow/databricks-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
