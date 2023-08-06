# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['curvepy', 'curvepy.extension']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.12.1,<0.13.0',
 'intervalpy>=0.1.0,<0.2.0',
 'numpy>=1.15.0,<2.0.0',
 'pyduration>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['test = pytest:main']}

setup_kwargs = {
    'name': 'curvepy',
    'version': '0.1.0',
    'description': 'A mathematical and financial function curve utility library.',
    'long_description': '# curvepy\n\n![Tests](https://github.com/diatche/curvepy/workflows/Tests/badge.svg)\n\nA mathematical and financial function curve utility library for Python.\n\n# Installation\n\nWith [poetry](https://python-poetry.org):\n\n```bash\npoetry add curvepy\n```\n\nOr with pip:\n\n```\npip3 install curvepy\n```\n\n# Usage\n\nHave a look at the [documentation](https://diatche.github.io/curvepy/).\n\nBasic usage:\n\n```python\n# Create a line\nfrom curvepy import Line\n\nline = Line(const=1, slope=2)\nassert line.y(0) == 1\nassert line.y(1) == 3\n\n# Function arithmetic\nline2 = Line(const=-1, slope=-2)\nline_sum = line1 + line2\nassert line_sum.y(0) == 0\nassert line_sum.y(1) == 0\n```\n\n# Development\n\n## Updating Documentation\n\nThe module [pdoc3](https://pdoc3.github.io/pdoc/) is used to automatically generate documentation. To update the documentation:\n\n1. Install `pdoc3` if needed with `pip3 install pdoc3`.\n2. Navigate to project root and install dependencies: `poetry install`.\n3. Generate documetation files with: `pdoc3 -o docs --html curvepy`.\n4. The new files will be in `docs/curvepy`. Move them to `docs/` and replace existing files.\n',
    'author': 'Pavel Diatchenko',
    'author_email': 'diatche@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/diatche/func',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4',
}


setup(**setup_kwargs)
