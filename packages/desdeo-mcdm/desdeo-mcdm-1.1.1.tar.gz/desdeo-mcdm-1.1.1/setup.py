# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['desdeo_mcdm', 'desdeo_mcdm.interactive', 'desdeo_mcdm.utilities']

package_data = \
{'': ['*']}

install_requires = \
['desdeo-problem>=1.0.0,<2.0.0', 'desdeo-tools>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'desdeo-mcdm',
    'version': '1.1.1',
    'description': 'Contains traditional optimization techniques from the field of Multiple-criteria decision-making. Methods belonging to the NIMBUS and NAUTILUS families can be found here. Part of the DESDEO framework.',
    'long_description': None,
    'author': 'Giovanni Misitano',
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
