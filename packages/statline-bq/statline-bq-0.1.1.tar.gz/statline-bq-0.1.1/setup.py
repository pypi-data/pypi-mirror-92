# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statline_bq']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'dask>=2.21.0,<3.0.0',
 'fsspec>=0.8.4,<0.9.0',
 'google-auth>=1.19.2,<2.0.0',
 'google-cloud-bigquery>=1.26.1,<2.0.0',
 'google-cloud-core>=1.3.0,<2.0.0',
 'google-cloud-storage>=1.30.0,<2.0.0',
 'pyarrow>=2.0.0,<3.0.0',
 'pyserde[toml]>=0.2.0,<0.3.0',
 'requests>=2.24.0,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'tomlkit>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['statline-bq = statline_bq.cli:upload_datasets']}

setup_kwargs = {
    'name': 'statline-bq',
    'version': '0.1.1',
    'description': 'Library to upload CBS open datasets into Google Cloud Platform',
    'long_description': None,
    'author': 'Daniel Kapitan',
    'author_email': 'daniel@kapitan.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://wijzijn.dedataverbinders.nl/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
