# Schemathesis 테스트 실행 방법:
#   1. poetry run python3 examples/schemathesis.py
#   2. poetry run schemathesis run http://localhost:8000/openapi.json

from __future__ import annotations

from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from starlette import status

app: FastAPI = FastAPI()


# 현재 FastAPI (0.110.0)는 파이썬 3.11이 기본으로 제공하는 OAS (OpenAPI Specification) 버전 (3.1.0)을 지원하지 않는다.
# 따라서, OAS 문서가 더 낮은 버전으로 생성되도록 custom_openapi 함수를 적용해야 한다.
def custom_openapi() -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema
    app.openapi_schema = get_openapi(
        title="Custom OpenAPI",
        version="3.0.2",
        openapi_version="3.0.2",
        description="Custom OpenAPI Schema",
        routes=app.routes,
    )
    return app.openapi_schema


app.openapi = custom_openapi


class User(BaseModel):
    name: str
    age: int
    roles: list[str] = ["user"]


_users: dict[str, User] = {}


@app.post("/user", status_code=status.HTTP_201_CREATED)
@app.post("/user/", status_code=status.HTTP_201_CREATED)
def create_user(user: User) -> User:
    _users[user.name] = user
    return user


@app.get("/user")
@app.get("/user/")
def get_all_users() -> list[User]:
    return list(_users.values())


@app.get("/user/{name}")
@app.get("/user/{name}/")
def get_user(name: str) -> User | None:
    return _users.get(name)


@app.put("/user/{name}")
@app.put("/user/{name}/")
def replace_user(name: str, user: User) -> User:
    if name != user.name:
        del _users[name]
    _users[user.name] = user
    return user


@app.patch("/user/{name}")
@app.patch("/user/{name}/")
def modify_user(name: str, user: User) -> User:
    if name != user.name:
        del _users[name]
    _users[user.name] = user
    return user


@app.delete("/user/{name}", status_code=status.HTTP_204_NO_CONTENT)
@app.delete("/user/{name}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(name: str) -> None:
    if _users.get(name) is not None:
        del _users[name]


if __name__ == "__main__":
    uvicorn.run("schemathesis:app", reload=True)
