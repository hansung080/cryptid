from __future__ import annotations

import itertools
from typing import Iterator

_counter: Iterator[int] = itertools.count(start=1)


def count() -> int:
    return next(_counter)
