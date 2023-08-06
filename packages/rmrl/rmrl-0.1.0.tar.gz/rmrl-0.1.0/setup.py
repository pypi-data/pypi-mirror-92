# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rmrl', 'rmrl.pens']

package_data = \
{'': ['*'],
 'rmrl.pens': ['paintbrush_png/*',
               'paintbrush_textures_log/*',
               'pencil_lin_png/*',
               'pencil_log_png/*',
               'pencil_textures_linear/*',
               'pencil_textures_log/*']}

install_requires = \
['pdfrw>=0.4,<0.5',
 'reportlab>=3.5.60,<4.0.0',
 'svglib>=1.0.1,<2.0.0',
 'xdg>=5.0.1,<6.0.0']

setup_kwargs = {
    'name': 'rmrl',
    'version': '0.1.0',
    'description': 'Render reMarkable documents to PDF',
    'long_description': None,
    'author': 'Robert Schroll',
    'author_email': 'rschroll@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
