# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bodas']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3,<4.0.0', 'numpy>=1.19.5,<2.0.0', 'sympy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'bodas',
    'version': '0.0.1',
    'description': 'Asymptotic Bode Plot in Python',
    'long_description': "## bodas\n\n![](https://github.com/urbanij/bodas/blob/main/docs/example1.png?raw=true)\n\n### Installation\n`pip install bodas`\n\n\n### Basic usage\n```python\nimport bodas\nimport sympy\n\ns = sympy.Symbol('s')\n\nH = 1/(1 + s/120)\n\nbodas.plot( str(H) )\n```\n",
    'author': 'Francesco Urbani',
    'author_email': 'francescourbanidue@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/urbanij/bodas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
