from __future__ import annotations

import os

if os.getenv("UNIT_TEST"):
    from examples.test_double import fake_mod1 as mod1
else:
    from examples.test_double import mod1  # type: ignore[no-redef]


def summer(x: int, y: int) -> str:
    return mod1.preamble() + f"{x + y}"
