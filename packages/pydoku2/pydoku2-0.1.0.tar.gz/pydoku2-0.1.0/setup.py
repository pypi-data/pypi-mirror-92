# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydoku2']

package_data = \
{'': ['*']}

install_requires = \
['Keras>=2.4.3,<3.0.0',
 'click>=7.1.2,<8.0.0',
 'numpy>=1.19.5,<2.0.0',
 'opencv-python>=4.5.1,<5.0.0',
 'tensorflow-cpu>=2.4.1,<3.0.0']

setup_kwargs = {
    'name': 'pydoku2',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'alexgQQ',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
