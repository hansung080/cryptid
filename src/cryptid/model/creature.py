from pydantic import BaseModel


class Creature(BaseModel):
    name: str
    country: str
    area: str
    description: str = ""
    aka: str = ""


class PartialCreature(BaseModel):
    name: str | None = None
    country: str | None = None
    area: str | None = None
    description: str | None = None
    aka: str | None = None
