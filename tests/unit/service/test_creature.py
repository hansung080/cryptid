import pytest

from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.creature import Creature
from cryptid.service import creature as service

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
    resp = service.create(yeti)
    assert resp == yeti


def test_create_already_exists(yeti: Creature) -> None:
    with pytest.raises(EntityAlreadyExistsError):
        _ = service.create(yeti)


def test_get_all() -> None:
    resp = service.get_all()
    assert len(resp) > 0


def test_get_one(yeti: Creature) -> None:
    resp = service.get_one(yeti.name)
    assert resp == yeti


def test_get_one_not_found(bigfoot: Creature) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = service.get_one(bigfoot.name)


def test_replace(yeti: Creature, bigfoot: Creature) -> None:
    resp = service.replace(yeti.name, bigfoot)
    assert resp == bigfoot


def test_replace_not_found(yeti: Creature) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = service.replace(yeti.name, yeti)


def test_modify(bigfoot: Creature) -> None:
    bigfoot.description = f"I'm Bigfoot {key_num}"
    resp = service.modify(bigfoot.name, bigfoot)
    assert resp == bigfoot


def test_modify_not_found(yeti: Creature) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = service.modify(yeti.name, yeti)


def test_delete(bigfoot: Creature) -> None:
    assert service.delete(bigfoot.name) is None


def test_delete_not_found(bigfoot: Creature) -> None:
    with pytest.raises(EntityNotFoundError):
        service.delete(bigfoot.name)
