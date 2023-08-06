# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['layer_analysis', 'layer_analysis.patchwise', 'layer_analysis.pixelwise']

package_data = \
{'': ['*']}

install_requires = \
['Keras==2.3.1', 'opencv-python>=4.5.1,<5.0.0', 'tensorflow==1.14.0']

setup_kwargs = {
    'name': 'layer-analysis',
    'version': '1.0a0',
    'description': '',
    'long_description': None,
    'author': 'deepio',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
