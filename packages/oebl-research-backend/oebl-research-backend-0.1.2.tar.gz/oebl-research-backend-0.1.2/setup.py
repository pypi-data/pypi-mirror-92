# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oebl_research_backend', 'oebl_research_backend.migrations']

package_data = \
{'': ['*']}

install_requires = \
['apis-core>=0.15.1,<0.16.0',
 'celery>=5.0.5,<6.0.0',
 'django-celery-results>=2.0.1,<3.0.0',
 'oebl-irs-workflow>=0.1.4,<0.2.0']

setup_kwargs = {
    'name': 'oebl-research-backend',
    'version': '0.1.2',
    'description': 'Backend for the GND backed research tool used in the ÖBL',
    'long_description': None,
    'author': 'Matthias Schlögl',
    'author_email': 'm.schloegl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
