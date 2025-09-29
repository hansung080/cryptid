from pydantic import BaseModel


class PublicUser(BaseModel):
    name: str
    roles: list[str] = ["user"]  # user, admin


class SignInUser(PublicUser):
    password: str


class PrivateUser(PublicUser):
    hash: str
