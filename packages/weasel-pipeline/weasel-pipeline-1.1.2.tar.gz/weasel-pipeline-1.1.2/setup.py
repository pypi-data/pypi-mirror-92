# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weasel_pipeline']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=6.7.1,<7.0.0',
 'configargparse>=1.2.3,<2.0.0',
 'uvloop>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'weasel-pipeline',
    'version': '1.1.2',
    'description': 'A minimalist pipelining framework for the WEASEL project.',
    'long_description': None,
    'author': 'Fabian Marquardt',
    'author_email': 'marquard@cs.uni-bonn.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
