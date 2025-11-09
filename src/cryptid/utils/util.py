import os


def getenv_or_raise(key: str) -> str:
    if (value := os.getenv(key)) is None:
        raise EnvironmentError(f"environment variable '{key}' required")
    return value
