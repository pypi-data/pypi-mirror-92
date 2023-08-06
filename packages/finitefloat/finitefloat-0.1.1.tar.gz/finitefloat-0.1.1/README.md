# finitefloat

[![PyPI](https://img.shields.io/pypi/v/finitefloat)](https://pypi.org/project/finitefloat/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/finitefloat)](https://pypi.org/project/finitefloat/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![license](https://img.shields.io/github/license/nekonoshiri/finitefloat)](https://github.com/nekonoshiri/finitefloat/blob/main/LICENSE)

Finite (non-nan, non-inf) float.

## Usage

```Python
import math

from finitefloat import NotFinite, finitefloat

value: finitefloat = finitefloat(0.1)

try:
    value = finitefloat(math.nan)
except NotFinite:
    print("The value is not finite.")
```

## API

### Module `finitefloat`

#### *class* `finitefloat(x: Union[SupportsFloat, SupportsIndex, str, bytes, bytearray])`

Subclass of `float`.
Raise `NotFinite` exception if `float(x)` is nan or ±inf.

#### *class* `NotFinite`

Subclass of `ValueError`.

