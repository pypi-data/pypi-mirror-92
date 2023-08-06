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
    'version': '0.1.1',
    'description': 'Render reMarkable documents to PDF',
    'long_description': "rmrl: reMarkable Rendering Library\n===================================\nrmrl is a Python library for rendering reMarkable documents to PDF files.\nIt takes the original PDF document and the files describing your annotations,\ncombining them to produce a document close to what reMarkable itself would\noutput.\n\nDemo\n----\nThe same notebook was rendered to a PDF via the reMarkable app and rmrl.\nThe resultant PDF files were converted to PNGs with ImageMagick at 300\ndpi.\n\n reMarkable output | rmrl output\n:-----------------:|:-----------:\n[![reMarkable](demo/app.png)](demo/app.png) | [![rmrl](demo/rmrl.png)](demo/rmrl.png)\n\nThe biggest differences are the lack of texture in the pencils and paintbrush,\nwhich we hope to address in the future.  The highlight color is also different,\nbut we feel the default color is too subtle.\n\nInstallation\n------------\nrmrl requires Python 3.7 or later.  If that's installed, the easiest installation\nis to do a\n```bash\npip install rmrl\n```\nAlternatively, you may clone this repository.  [Poetry](https://python-poetry.org/) is used for development, so once that is installed you can run\n```bash\npoetry install\n```\nto get a virtual environment all set up.\n\nUsage\n-----\nThe main interface to rmrl is through a single function:\n```python\nfrom rmrl import render\n\noutput = render(source)\n```\n`source` may be:\n- The filename of a zip file containing the document.\n- The filename of any (root-level) file from an unpacked document.\n- Any object that provides `open()` and `exists()` methods.  See\n  `rmrl/sources.py` for more details on this API.\n\nThe output is a filestream with the contents of the PDF file.\n\nThe `render` function takes the following keyword arguments:\n- `progress_cb`: A callback function to be called periodically during the\n  rendering process.  It will be called with a single argument, a number\n  from 0 to 100 indicating the progress.  This function can abort the\n  process by raising an exception.\n\nCommand-line Usage\n------------------\nrmrl may be called as a command-line tool.  Once it has been installed, run\n```bash\npython -m rmrl filename\n```\nto convert `filename` to an annotated PDF.  The default output is to stdout.\nUse\n```bash\npython -m rmrl -h\n```\nto see all of the options.\n\nTemplates\n---------\nrmrl can use the reMarkable templates as a background when rendering notebooks.\nWe cannot ship copies of these templates.  You may be allowed to copy them from\nyour own reMarkable device on to your computer for personal use.  If this is\nlegal in your jurisdiction, you may connect your device to your computer by the\nUSB cable and run\n```bash\npython -m rmrl.load_templates\n```\nThis will copy these templates to `~/.local/share/rmrl/templates` (assuming\ndefault XDG settings).\n\nHistory\n-------\nrmrl derives from the [reMarkable Connection Utility](http://www.davisr.me/projects/rcu/),\nby Davis Remmel.  RCU is a full-featured GUI for managing all aspects of a\nreMarkable device.  Do check it out if you are looking for a stand-alone\nsolution for getting documents on and off of your device.\n\nRCU was chosen as a base for rmrl due to its high-quality rendering.  The\nfollowing are the major changes:\n- rmrl is designed as a library, for incorporation into other programs.  RCU\n  is designed as a stand-alone program.\n- rmrl uses the pure-Python [ReportLab Toolkit](https://www.reportlab.com/dev/opensource/rl-toolkit/)\n  for rendering PDF files.  RCU uses the Qt framework, which is a significantly\n  heavier installation.\n- rmrl only supports vector output, while RCU offers both raster and vector\n  rendering.\n- RCU supports PDF layers (Optional Content Groups).  At this point, rmrl does\n  not.\n- RCU can add PDF annotations corresponding to highlights.  At this point, rmrl\n  does not.\n\nTrademarks\n----------\nreMarkable(R) is a registered trademark of reMarkable AS. rmrl is not\naffiliated with, or endorsed by, reMarkable AS. The use of “reMarkable”\nin this work refers to the company’s e-paper tablet product(s).\n\nCopyright\n---------\nCopyright (C) 2020  Davis Remmel\n\nCopyright 2021 Robert Schroll\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <https://www.gnu.org/licenses/>.\n",
    'author': 'Robert Schroll',
    'author_email': 'rschroll@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rschroll/rmrl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
