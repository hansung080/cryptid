from pydantic import BaseModel, field_validator


class Creature(BaseModel):
    name: str
    country: str
    area: str
    description: str = ""
    aka: str = ""

    @field_validator("name")
    @staticmethod
    def validate_name(name: str) -> str:
        name = name.strip()
        if not name:
            raise ValueError("field 'name' cannot be empty or whitespace")
        return name


class PartialCreature(BaseModel):
    name: str | None = None
    country: str | None = None
    area: str | None = None
    description: str | None = None
    aka: str | None = None

    @field_validator("name")
    @staticmethod
    def validate_name(name: str | None) -> str | None:
        if name is None:
            return None
        return Creature.validate_name(name)

