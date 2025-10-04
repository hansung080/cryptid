from pydantic import BaseModel


class Explorer(BaseModel):
    name: str
    country: str
    description: str = ""


class PartialExplorer(BaseModel):
    name: str | None = None
    country: str | None = None
    description: str | None = None
