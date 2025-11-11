from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient
from httpx import Response
from pydantic import BaseModel
from starlette import status

from cryptid.main import app
from cryptid.model.auth import TokenResponse
from cryptid.model.user import PublicUser, SignInUser

from tests.common import count

key_num: int = count()
client: TestClient = TestClient(app)


def assert_response(
    resp: Response,
    *,
    status_code: int,
    json: BaseModel | None = None,
    body_none: bool = False
) -> None:
    assert resp.status_code == status_code
    if json is None:
        if body_none:
            assert resp.content == b""
    else:
        assert resp.json() == json.model_dump()


def make_headers(*, token: str | None = None) -> dict[str, Any]:
    headers = {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def create_user(user: SignInUser) -> PublicUser:
    resp = client.post("/users", json=user.model_dump())
    assert resp.status_code == status.HTTP_201_CREATED
    resp_user = PublicUser.model_validate(resp.json())
    user.id = resp_user.id
    user.created_at = resp_user.created_at
    user.updated_at = resp_user.updated_at
    return resp_user


def create_token(user: SignInUser) -> TokenResponse:
    resp = client.post("/auth/token", data={"username": user.id, "password": user.password})
    assert resp.status_code == status.HTTP_201_CREATED
    return TokenResponse.model_validate(resp.json())


admin = SignInUser(
    name=f"Admin {key_num}",
    roles=["admin"],
    password="admin1234",
)
create_user(admin)
admin_token: str = create_token(admin).access
