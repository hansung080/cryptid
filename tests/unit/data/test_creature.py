import pytest

import cryptonamicon.data.creature as data
from cryptonamicon.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptonamicon.model.creature import Creature

from tests.common import count

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
    resp = data.create(yeti)
    assert resp == yeti


def test_create_already_exists(yeti: Creature) -> None:
    with pytest.raises(EntityAlreadyExistsError):
        _ = data.create(yeti)


def test_get_all() -> None:
    resp = data.get_all()
    assert len(resp) > 0


def test_get_one(yeti: Creature) -> None:
    resp = data.get_one(yeti.name)
    assert resp == yeti


def test_get_one_not_found(bigfoot: Creature) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = data.get_one(bigfoot.name)


def test_modify(yeti: Creature, bigfoot: Creature) -> None:
    resp = data.modify(yeti.name, bigfoot)
    assert resp == bigfoot


def test_modify_not_found(yeti: Creature) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = data.modify(yeti.name, yeti)


def test_delete(bigfoot: Creature) -> None:
    assert data.delete(bigfoot.name) is None


def test_delete_not_found(bigfoot: Creature) -> None:
    with pytest.raises(EntityNotFoundError):
        data.delete(bigfoot.name)
