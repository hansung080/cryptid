from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from starlette import status

from cryptid.main import app
from cryptid.model.creature import Creature, PartialCreature

from tests.common import count
from tests.full.common import admin_token, assert_response, make_headers

key_num: int = count()
client: TestClient = TestClient(app)


@pytest.fixture
def yeti() -> Creature:
    return Creature(
        name=f"Yeti {key_num}",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
        aka="Abominable Snowman",
    )


@pytest.fixture
def bigfoot() -> Creature:
    return Creature(
        name=f"Bigfoot {key_num}",
        country="US",
        area="*",
        description="Yeti's Cousin Eddie",
        aka="Sasquatch",
    )


def test_create(yeti: Creature) -> None:
    resp = client.post("/creatures", headers=make_headers(token=admin_token), json=yeti.model_dump())
    assert_response(resp, status_code=status.HTTP_201_CREATED, json=yeti)


def test_create_already_exists(yeti: Creature) -> None:
    resp = client.post("/creatures", headers=make_headers(token=admin_token), json=yeti.model_dump())
    assert_response(resp, status_code=status.HTTP_409_CONFLICT)


def test_get_all() -> None:
    resp = client.get("/creatures")
    assert_response(resp, status_code=status.HTTP_200_OK)


def test_get_one(yeti: Creature) -> None:
    resp = client.get(f"/creatures/{yeti.name}")
    assert_response(resp, status_code=status.HTTP_200_OK, json=yeti)


def test_get_one_not_found(bigfoot: Creature) -> None:
    resp = client.get(f"/creatures/{bigfoot.name}")
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_replace(yeti: Creature, bigfoot: Creature) -> None:
    resp = client.put(f"/creatures/{yeti.name}", headers=make_headers(token=admin_token), json=bigfoot.model_dump())
    assert_response(resp, status_code=status.HTTP_200_OK, json=bigfoot)


def test_replace_not_found(yeti: Creature) -> None:
    resp = client.put(f"/creatures/{yeti.name}", headers=make_headers(token=admin_token), json=yeti.model_dump())
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_modify(bigfoot: Creature) -> None:
    bigfoot.description = f"I'm Bigfoot {key_num}"
    creature = PartialCreature(description=bigfoot.description).model_dump(exclude_unset=True)
    resp = client.patch(f"/creatures/{bigfoot.name}", headers=make_headers(token=admin_token), json=creature)
    assert_response(resp, status_code=status.HTTP_200_OK, json=bigfoot)


def test_modify_not_found(yeti: Creature) -> None:
    creature = PartialCreature().model_dump(exclude_unset=True)
    resp = client.patch(f"/creatures/{yeti.name}", headers=make_headers(token=admin_token), json=creature)
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)


def test_delete(bigfoot: Creature) -> None:
    resp = client.delete(f"/creatures/{bigfoot.name}", headers=make_headers(token=admin_token))
    assert_response(resp, status_code=status.HTTP_204_NO_CONTENT, body_none=True)


def test_delete_not_found(bigfoot: Creature) -> None:
    resp = client.delete(f"/creatures/{bigfoot.name}", headers=make_headers(token=admin_token))
    assert_response(resp, status_code=status.HTTP_404_NOT_FOUND)
