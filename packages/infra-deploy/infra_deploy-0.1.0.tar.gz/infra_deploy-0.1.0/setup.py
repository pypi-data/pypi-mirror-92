# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['infra_deploy',
 'infra_deploy.experimental',
 'infra_deploy.metadata',
 'infra_deploy.metadata.decorators',
 'infra_deploy.metadata.kubevela',
 'infra_deploy.models',
 'infra_deploy.models.ambassador',
 'infra_deploy.models.argocd',
 'infra_deploy.models.resources',
 'infra_deploy.validation',
 'infra_deploy.workflows',
 'infra_deploy.workflows.dsl']

package_data = \
{'': ['*'],
 'infra_deploy': ['examples/*'],
 'infra_deploy.models.ambassador': ['schemas/*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'addict>=2.4.0,<3.0.0',
 'argo-workflows>=5.0.0,<6.0.0',
 'auto-all>=1.3.0,<2.0.0',
 'cachetools>=4.2.0,<5.0.0',
 'confuse>=1.4.0,<2.0.0',
 'cytoolz>=0.11.0,<0.12.0',
 'decopatch>=1.4.8,<2.0.0',
 'decorator>=4.4.2,<5.0.0',
 'inflection>=0.5.1,<0.6.0',
 'kubernetes>=12.0.1,<13.0.0',
 'loguru>=0.5.3,<0.6.0',
 'makefun>=1.9.5,<2.0.0',
 'mypy-extensions>=0.4.3,<0.5.0',
 'orjson>=3.4.7,<4.0.0',
 'pick>=1.0.0,<2.0.0',
 'pybase64>=1.1.3,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'varname>=0.5.6,<0.6.0']

setup_kwargs = {
    'name': 'infra-deploy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Kevin Hill',
    'author_email': 'kah.kevin.hill@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
