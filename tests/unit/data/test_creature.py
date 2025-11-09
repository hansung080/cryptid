import pytest

from cryptid.data import creature as data
from cryptid.data.init import Cursor, get_cursor, transaction_with
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.creature import Creature, PartialCreature

from tests.common import count

key_num: int = count()


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
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        resp = data.create(cursor, yeti)
        assert resp == yeti
    inner()


def test_create_already_exists(yeti: Creature) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        with pytest.raises(EntityAlreadyExistsError):
            _ = data.create(cursor, yeti)
    inner()


def test_get_all() -> None:
    resp = data.get_all(get_cursor())
    assert len(resp) > 0


def test_get_one(yeti: Creature) -> None:
    resp = data.get_one(get_cursor(), yeti.name)
    assert resp == yeti


def test_get_one_not_found(bigfoot: Creature) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = data.get_one(get_cursor(), bigfoot.name)


def test_replace(yeti: Creature, bigfoot: Creature) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        resp = data.replace(cursor, yeti.name, bigfoot)
        assert resp == bigfoot
    inner()


def test_replace_not_found(yeti: Creature) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        with pytest.raises(EntityNotFoundError):
            _ = data.replace(cursor, yeti.name, yeti)
    inner()


def test_modify(bigfoot: Creature) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        bigfoot.description = f"I'm Bigfoot {key_num}"
        resp = data.modify(cursor, bigfoot.name, PartialCreature(description=bigfoot.description))
        assert resp == bigfoot
    inner()


def test_modify_not_found(yeti: Creature) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        with pytest.raises(EntityNotFoundError):
            _ = data.modify(cursor, yeti.name, PartialCreature())
    inner()


def test_delete(bigfoot: Creature) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        assert data.delete(cursor, bigfoot.name) is None
    inner()


def test_delete_not_found(bigfoot: Creature) -> None:
    @transaction_with(new_conn=False)
    def inner(cursor: Cursor) -> None:
        with pytest.raises(EntityNotFoundError):
            data.delete(cursor, bigfoot.name)
    inner()
