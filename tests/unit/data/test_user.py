import pytest

from cryptid.data import user as data
from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.user import PublicUser, PrivateUser, PartialUser
from cryptid.service.auth import make_hash

from tests.common import count

key_num = count()


@pytest.fixture
def mike() -> PublicUser:
    return PublicUser(
        name=f"Mike {key_num}",
        roles=["user", "admin"],
    )


@pytest.fixture
def mike_password() -> str:
    return "1234"


@pytest.fixture
def john() -> PublicUser:
    return PublicUser(
        name=f"John {key_num}",
        roles=["user"],
    )


def test_create(mike: PublicUser, mike_password: str) -> None:
    user = PrivateUser(
        name=mike.name,
        roles=mike.roles,
        hash=make_hash(mike_password),
    )
    resp = data.create(user)
    assert resp == mike


def test_create_already_exists(mike: PublicUser, mike_password: str) -> None:
    user = PrivateUser(
        name=mike.name,
        roles=mike.roles,
        hash=make_hash(mike_password),
    )
    with pytest.raises(EntityAlreadyExistsError):
        _ = data.create(user)


def test_get_all() -> None:
    resp = data.get_all()
    assert len(resp) > 0


def test_get_one(mike: PublicUser) -> None:
    resp = data.get_one(mike.name)
    assert resp == mike


def test_get_one_not_found(john: PublicUser) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = data.get_one(john.name)


def test_replace(mike: PublicUser, john: PublicUser) -> None:
    resp = data.replace(mike.name, john)
    assert resp == john


def test_replace_not_found(mike: PublicUser) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = data.replace(mike.name, mike)


def test_modify(john: PublicUser) -> None:
    john.roles = ["user", "admin"]
    resp = data.modify(john.name, PartialUser(roles=john.roles))
    assert resp == john


def test_modify_not_found(mike: PublicUser) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = data.modify(mike.name, PartialUser())


def test_delete(john: PublicUser) -> None:
    assert data.delete(john.name) is None
    resp = data.get_one(john.name, deleted_user=True)
    john.roles = ["user", "admin"]
    assert resp == john


def test_delete_not_found(john: PublicUser) -> None:
    with pytest.raises(EntityNotFoundError):
        data.delete(john.name)
