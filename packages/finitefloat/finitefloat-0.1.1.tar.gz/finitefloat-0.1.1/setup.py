# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['finitefloat']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'finitefloat',
    'version': '0.1.1',
    'description': 'Finite (non-nan, non-inf) float',
    'long_description': '# finitefloat\n\n[![PyPI](https://img.shields.io/pypi/v/finitefloat)](https://pypi.org/project/finitefloat/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/finitefloat)](https://pypi.org/project/finitefloat/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![license](https://img.shields.io/github/license/nekonoshiri/finitefloat)](https://github.com/nekonoshiri/finitefloat/blob/main/LICENSE)\n\nFinite (non-nan, non-inf) float.\n\n## Usage\n\n```Python\nimport math\n\nfrom finitefloat import NotFinite, finitefloat\n\nvalue: finitefloat = finitefloat(0.1)\n\ntry:\n    value = finitefloat(math.nan)\nexcept NotFinite:\n    print("The value is not finite.")\n```\n\n## API\n\n### Module `finitefloat`\n\n#### *class* `finitefloat(x: Union[SupportsFloat, SupportsIndex, str, bytes, bytearray])`\n\nSubclass of `float`.\nRaise `NotFinite` exception if `float(x)` is nan or \xc2\xb1inf.\n\n#### *class* `NotFinite`\n\nSubclass of `ValueError`.\n\n',
    'author': 'Shiri Nekono',
    'author_email': 'gexira.halen.toms@gmail.com',
    'maintainer': 'Shiri Nekono',
    'maintainer_email': 'gexira.halen.toms@gmail.com',
    'url': 'https://github.com/nekonoshiri/finitefloat',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
