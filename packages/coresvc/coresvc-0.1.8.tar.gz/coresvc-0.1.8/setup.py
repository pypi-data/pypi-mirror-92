# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coresvc',
 'coresvc.base',
 'coresvc.comm',
 'coresvc.crud',
 'coresvc.datastore',
 'coresvc.serializer',
 'coresvc.util']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.22,<2.0.0',
 'aio-pika>=6.7.1,<7.0.0',
 'aioredis>=1.3.1,<2.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'faust>=1.10.4,<2.0.0',
 'psycopg2>=2.8.6,<3.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'uvicorn[standard]>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'coresvc',
    'version': '0.1.8',
    'description': 'core services in microservice architecture',
    'long_description': None,
    'author': 'MartinJ-Dev',
    'author_email': '29751536+MartinJ-Dev@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
