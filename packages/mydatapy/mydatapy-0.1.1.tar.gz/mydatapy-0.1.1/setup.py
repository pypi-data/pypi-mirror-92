# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mydatapy', 'mydatapy.models', 'mydatapy.templates']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'requests-xml>=0.2.3,<0.3.0',
 'requests>=2.25.1,<3.0.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'mydatapy',
    'version': '0.1.1',
    'description': 'A simple wrapper of mydata platform of greek tax registry',
    'long_description': None,
    'author': 'Dimitrios Strantsalis',
    'author_email': 'dstrants@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
