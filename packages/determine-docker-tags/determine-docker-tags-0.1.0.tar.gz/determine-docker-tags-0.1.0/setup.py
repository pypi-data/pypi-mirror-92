# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['determine_docker_tags']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['determine-docker-tags = '
                     'determine_docker_tags.__init__:main']}

setup_kwargs = {
    'name': 'determine-docker-tags',
    'version': '0.1.0',
    'description': '',
    'long_description': '# docker-determine-tags\n',
    'author': 'Magnus Walbeck',
    'author_email': 'magnus.walbeck@walbeck.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
