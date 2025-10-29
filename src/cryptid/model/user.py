from datetime import datetime

from pydantic import BaseModel, field_validator


class PublicUser(BaseModel):
    id: str | None = None
    name: str
    roles: list[str] = ["user"]  # user, admin
    created_at: datetime | None = None  # UTC
    updated_at: datetime | None = None  # UTC
    deleted_at: datetime | None = None  # UTC

    # Ignore the following warning from IntelliJ IDEA, which is a wrong inspection (false-positive warning).
    # Warning: This decorator will not receive a callable it may expect; the built-in decorator returns a special object
    @field_validator("name")
    @staticmethod
    def validate_name(name: str) -> str:
        name = name.strip()
        if not name:
            raise ValueError("field 'name' cannot be empty or whitespace")
        if name == "me":
            raise ValueError("field 'name' cannot be the reserved keyword 'me'")
        return name


class SignInUser(PublicUser):
    password: str

    @field_validator("password")
    @staticmethod
    def validate_password(password: str):
        password = password.strip()
        if not password:
            return ValueError("field 'password' cannot be empty or whitespace")
        return password


class PrivateUser(PublicUser):
    hash: str


class PartialUser(BaseModel):
    name: str | None = None
    roles: list[str] | None = None

    @field_validator("name")
    @staticmethod
    def validate_name(name: str | None) -> str | None:
        if name is None:
            return None
        return PublicUser.validate_name(name)
