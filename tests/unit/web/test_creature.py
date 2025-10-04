import pytest
from fastapi import HTTPException

from cryptid.model.creature import Creature, PartialCreature
from cryptid.web import creature as web

from tests.common import count
from tests.unit.web.common import assert_already_exists_error, assert_not_found_error

key_num = count()


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
    resp = web.create(yeti)
    assert resp == yeti


def test_create_already_exists(yeti: Creature) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.create(yeti)
        assert_already_exists_error(e)


def test_get_all() -> None:
    resp = web.get_all()
    assert len(resp) > 0


def test_get_one(yeti: Creature) -> None:
    resp = web.get_one(yeti.name)
    assert resp == yeti


def test_get_one_not_found(bigfoot: Creature) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.get_one(bigfoot.name)
        assert_not_found_error(e)


def test_replace(yeti: Creature, bigfoot: Creature) -> None:
    resp = web.replace(yeti.name, bigfoot)
    assert resp == bigfoot


def test_replace_not_found(yeti: Creature) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.replace(yeti.name, yeti)
        assert_not_found_error(e)


def test_modify(bigfoot: Creature) -> None:
    bigfoot.description = f"I'm Bigfoot {key_num}"
    resp = web.modify(bigfoot.name, PartialCreature(description=bigfoot.description))
    assert resp == bigfoot


def test_modify_not_found(yeti: Creature) -> None:
    with pytest.raises(HTTPException) as e:
        _ = web.modify(yeti.name, PartialCreature())
        assert_not_found_error(e)


def test_delete(bigfoot: Creature) -> None:
    assert web.delete(bigfoot.name) is None


def test_delete_not_found(bigfoot: Creature) -> None:
    with pytest.raises(HTTPException) as e:
        web.delete(bigfoot.name)
        assert_not_found_error(e)
