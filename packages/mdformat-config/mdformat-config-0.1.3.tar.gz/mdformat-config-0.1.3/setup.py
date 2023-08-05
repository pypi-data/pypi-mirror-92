# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdformat_config']

package_data = \
{'': ['*']}

install_requires = \
['mdformat>=0.3.0', 'ruamel.yaml>=0.16.0', 'toml>=0.10.0']

entry_points = \
{'mdformat.codeformatter': ['json = mdformat_config:format_json',
                            'toml = mdformat_config:format_toml',
                            'yaml = mdformat_config:format_yaml']}

setup_kwargs = {
    'name': 'mdformat-config',
    'version': '0.1.3',
    'description': 'Mdformat plugin to beautify configuration and data-serialization formats',
    'long_description': '[![Build Status](https://github.com/hukkinj1/mdformat-config/workflows/Tests/badge.svg?branch=master)](<https://github.com/hukkinj1/mdformat-config/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush>)\n[![PyPI version](https://img.shields.io/pypi/v/mdformat-config)](https://pypi.org/project/mdformat-config)\n\n# mdformat-config\n> Mdformat plugin to beautify configuration and data-serialization formats\n\n## Description\nmdformat-config is an [mdformat](https://github.com/executablebooks/mdformat) plugin\nthat makes mdformat beautify configuration and data-serialization formats.\nCurrently supported formats are JSON, TOML and YAML.\n\n## Installing\n```bash\npip install mdformat-config\n```\n\n## Usage\n```bash\nmdformat YOUR_MARKDOWN_FILE.md\n```\n',
    'author': 'Taneli Hukkinen',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/mdformat-config',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
