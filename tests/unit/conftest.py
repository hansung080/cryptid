import os


# The `pytest_configure` hook occurs before running the `import` statement in test modules.
def pytest_configure() -> None:
    os.environ["CRYPTID_UNIT_TEST"] = "true"


# The `pytest.fixture` hook occurs after running the `import` statement in test modules.
# import pytest
# @pytest.fixture(autouse=True, scope="session")
# def set_env() -> None:
#     os.environ["CRYPTID_UNIT_TEST"] = "true"
