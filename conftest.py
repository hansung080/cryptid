import subprocess

import pytest


def pytest_cmdline_main(config: pytest.Config) -> int | None:
    args = config.invocation_params.args
    if not args or args[0] == "tests":
        cmds = [
            ["pytest", "tests/unit"],
            ["pytest", "tests/full"],
        ]
        for cmd in cmds:
            result = subprocess.run(cmd)
            if result.returncode != 0:
                return result.returncode
        return 0
