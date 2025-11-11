from __future__ import annotations

import os

from dotenv import load_dotenv


def getenv_or_raise(key: str) -> str:
    if (value := os.getenv(key)) is None:
        raise EnvironmentError(f"environment variable '{key}' required")
    return value


load_dotenv()

JWT_ALGORITHM: str = os.getenv("CRYPTID_JWT_ALGORITHM", default="HS256")
JWT_EXPIRES_IN_MINUTES: float = float(os.getenv("CRYPTID_JWT_EXPIRES_IN_MINUTES", default="15"))
JWT_SECRET_KEY: str = getenv_or_raise("CRYPTID_JWT_SECRET_KEY")
