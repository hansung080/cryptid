import os


def pytest_configure() -> None:
    os.environ["CRYPTID_UNIT_TEST"] = ""
