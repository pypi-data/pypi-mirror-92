# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpyanalytics', 'jrpyanalytics.datasets']

package_data = \
{'': ['*'],
 'jrpyanalytics': ['vignettes/*'],
 'jrpyanalytics.datasets': ['data/*']}

install_requires = \
['graphviz>=0.10.1,<0.11.0',
 'jrpytests>=0.1.4,<0.2.0',
 'matplotlib>=3.0,<4.0',
 'numpy>=1.15,<2.0',
 'pandas>=1,<2',
 'seaborn>=0.11.0,<0.12.0',
 'sklearn>=0.0.0,<0.0.1']

setup_kwargs = {
    'name': 'jrpyanalytics',
    'version': '0.1.8',
    'description': 'Jumping Rivers: Predictive Analytics in Python',
    'long_description': None,
    'author': 'Jamie',
    'author_email': 'jamie@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
