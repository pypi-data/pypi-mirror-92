# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_buzz']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.0,<2.0', 'py-buzz>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'flask-buzz',
    'version': '1.0.0',
    'description': "'Extra bindings on py-buzz specifically for flask apps'",
    'long_description': None,
    'author': 'Tucker Beck',
    'author_email': 'tucker.beck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
