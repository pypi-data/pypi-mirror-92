# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdformat_shfmt']

package_data = \
{'': ['*']}

install_requires = \
['mdformat>=0.3.5']

entry_points = \
{'mdformat.codeformatter': ['bash = mdformat_shfmt:format_sh',
                            'sh = mdformat_shfmt:format_sh']}

setup_kwargs = {
    'name': 'mdformat-shfmt',
    'version': '0.1.0',
    'description': 'Mdformat plugin to format shell code blocks',
    'long_description': '[![Build Status](https://github.com/hukkinj1/mdformat-shfmt/workflows/Tests/badge.svg?branch=master)](<https://github.com/hukkinj1/mdformat-shfmt/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush>)\n[![PyPI version](<https://img.shields.io/pypi/v/mdformat-shfmt>)](<https://pypi.org/project/mdformat-shfmt>)\n\n# mdformat-shfmt\n> Mdformat plugin to format shell code blocks\n\n## Description\nmdformat-shfmt is an [mdformat](https://github.com/executablebooks/mdformat) plugin\nthat makes mdformat format shell code blocks embedded in Markdown with [shfmt](https://github.com/mvdan/sh).\nThe plugin invokes shfmt in a subprocess so having either shfmt or Docker installed is a requirement.\n\n## Installing\n1. Install either [shfmt](https://github.com/mvdan/sh#shfmt) or [Docker](https://docs.docker.com/get-docker/)\n1. Install mdformat-shfmt\n   ```bash\n   pip install mdformat-shfmt\n   ```\n\n## Usage\n```bash\nmdformat YOUR_MARKDOWN_FILE.md\n```\n\n## Limitations\nFormatting with Docker is not tested on Windows.\nIf you experience issues on Windows, install shfmt.\n',
    'author': 'Taneli Hukkinen',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/mdformat-shfmt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
