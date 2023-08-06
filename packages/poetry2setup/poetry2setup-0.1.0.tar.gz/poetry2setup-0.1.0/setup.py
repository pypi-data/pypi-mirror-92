# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['poetry2setup']
install_requires = \
['poetry-core>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['poetry2setup = poetry2setup:main']}

setup_kwargs = {
    'name': 'poetry2setup',
    'version': '0.1.0',
    'description': 'Convert python-poetry to setup.py',
    'long_description': 'Convert python-poetry(pyproject.toml) to setup.py.\n\nIt only relies on poetry.core, so the effect is better than any other third-party software.\n\nI created this library because python-poetry does not support exporting to setup.py and dephell will generate setup.py incorrectly in some cases.\n\n## Install\n\n```bash\npip install poetry2setup\n```\n\n## Usage\n\nRun command `poetry2setup` in your project directory, it will display `setup.py` content in console. If you want to export to `setup.py`, just run `poetry2setup > setup.py`.\n',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
