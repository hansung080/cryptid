from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, model_serializer


class Token(BaseModel):
    access: str
    type: str = "bearer"
    expires_in_seconds: int | None = None
    expires_at: datetime | None = None
    issued_at: datetime
    refresh: str | None = None


class TokenResponse(BaseModel):
    access: str = Field(..., alias="access_token")
    type: str = Field("bearer", alias="token_type")
    expires_in_seconds: int | None = Field(None, alias="expires_in")
    refresh: str | None = Field(None, alias="refresh_token")

    model_config = ConfigDict(populate_by_name=True)

    @model_serializer(mode="wrap")
    def serialize(self, handler):
        data = handler(self)
        if self.refresh is None:
            data.pop("refresh_token", None)
        return data


class AuthUser(BaseModel):
    id: str
    roles: list[str]
