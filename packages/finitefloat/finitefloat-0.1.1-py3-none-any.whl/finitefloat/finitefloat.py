from __future__ import annotations

from math import isfinite
from typing import SupportsFloat, SupportsIndex, Union

from .exceptions import NotFinite


class finitefloat(float):
    def __new__(
        cls, x: Union[SupportsFloat, SupportsIndex, str, bytes, bytearray]
    ) -> finitefloat:
        f = float(x)
        if not isfinite(f):
            raise NotFinite
        return float.__new__(finitefloat, f)
