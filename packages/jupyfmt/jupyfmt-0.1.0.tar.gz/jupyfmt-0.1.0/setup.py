# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupyfmt']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0',
 'click>=7.1.2,<8.0.0',
 'ipython>=7.19.0,<8.0.0',
 'nbformat>=5.1.2,<6.0.0']

setup_kwargs = {
    'name': 'jupyfmt',
    'version': '0.1.0',
    'description': 'Format code in Jupyter notebooks',
    'long_description': '# jupyfmt\n\n[![PyPI](https://img.shields.io/pypi/v/jupyfmt.svg?style=flat)](https://pypi.python.org/pypi/jupyfmt)\n[![Tests](https://github.com/kpj/jupyfmt/workflows/Tests/badge.svg)](https://github.com/kpj/jupyfmt/actions)\n\nFormat code in Jupyter notebooks.\n\n[jupyter-black](https://github.com/drillan/jupyter-black) and [nb_black](https://github.com/dnanhkhoa/nb_black) are fabulous Jupyter extensions for formatting your code in the editor.\n`jupyfmt` allows you to assert properly formatted Jupyter notebook cells in your CI.\n\n\n## Installation\n\n```python\n$ pip install jupyfmt\n```\n\n\n## Usage\n\n```bash\n$ jupyfmt Notebook.ipynb\n```\n',
    'author': 'kpj',
    'author_email': 'kim.philipp.jablonski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kpj/jupyfmt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
