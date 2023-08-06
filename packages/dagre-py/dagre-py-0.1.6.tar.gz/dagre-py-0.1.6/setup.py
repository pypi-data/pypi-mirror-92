# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dagre_py']

package_data = \
{'': ['*'], 'dagre_py': ['js/*']}

setup_kwargs = {
    'name': 'dagre-py',
    'version': '0.1.6',
    'description': 'Thin python wrapper around dagre-d3',
    'long_description': None,
    'author': 'Abhinav Tushar',
    'author_email': 'abhinav@vernacular.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Vernacular-ai/dagre-py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
