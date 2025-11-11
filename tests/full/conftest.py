from __future__ import annotations

import os


def pytest_configure() -> None:
    os.environ["CRYPTID_UNIT_TEST"] = ""
