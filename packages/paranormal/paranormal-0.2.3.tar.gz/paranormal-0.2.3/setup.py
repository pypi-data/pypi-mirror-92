# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paranormal', 'paranormal.test']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1', 'numpy>1.18', 'pampy>=0.2.1']

setup_kwargs = {
    'name': 'paranormal',
    'version': '0.2.3',
    'description': 'Coherent management of large parameter lists in Python',
    'long_description': None,
    'author': 'Schuyler Fried',
    'author_email': 'schuylerfried@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.6',
}


setup(**setup_kwargs)
