from __future__ import annotations

from pydantic import BaseModel, field_validator


class Explorer(BaseModel):
    name: str
    country: str
    description: str = ""

    @field_validator("name")
    @staticmethod
    def validate_name(name: str) -> str:
        name = name.strip()
        if not name:
            raise ValueError("field 'name' cannot be empty or whitespace")
        return name


class PartialExplorer(BaseModel):
    name: str | None = None
    country: str | None = None
    description: str | None = None

    @field_validator("name")
    @staticmethod
    def validate_name(name: str | None) -> str | None:
        if name is None:
            return None
        return Explorer.validate_name(name)
