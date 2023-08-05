# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdformat_rustfmt']

package_data = \
{'': ['*']}

install_requires = \
['mdformat>=0.3.5']

entry_points = \
{'mdformat.codeformatter': ['rust = mdformat_rustfmt:format_rust']}

setup_kwargs = {
    'name': 'mdformat-rustfmt',
    'version': '0.0.3',
    'description': 'Mdformat plugin to rustfmt Rust code blocks',
    'long_description': '[![Build Status](https://github.com/hukkinj1/mdformat-rustfmt/workflows/Tests/badge.svg?branch=master)](<https://github.com/hukkinj1/mdformat-rustfmt/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush>)\n[![PyPI version](<https://img.shields.io/pypi/v/mdformat-rustfmt>)](<https://pypi.org/project/mdformat-rustfmt>)\n\n# mdformat-rustfmt\n> Mdformat plugin to rustfmt Rust code blocks\n\n## Description\nmdformat-rustfmt is an [mdformat](https://github.com/executablebooks/mdformat) plugin\nthat makes mdformat format Rust code blocks with [rustfmt](https://github.com/rust-lang/rustfmt).\nThe plugin invokes rustfmt in a subprocess so having it installed is a requirement.\n\n## Installing\n1. [Install rustfmt](https://github.com/rust-lang/rustfmt#quick-start)\n1. Install mdformat-rustfmt\n   ```bash\n   pip install mdformat-rustfmt\n   ```\n\n## Usage\n```bash\nmdformat YOUR_MARKDOWN_FILE.md\n```\n',
    'author': 'Taneli Hukkinen',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/mdformat-rustfmt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
