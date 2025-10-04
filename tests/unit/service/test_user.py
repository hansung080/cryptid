import pytest

from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.user import PublicUser, SignInUser, PartialUser
from cryptid.service import user as service

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
    user = SignInUser(
        name=mike.name,
        roles=mike.roles,
        password=mike_password,
    )
    resp = service.create(user)
    assert resp == mike


def test_create_already_exists(mike: PublicUser, mike_password: str) -> None:
    user = SignInUser(
        name=mike.name,
        roles=mike.roles,
        password=mike_password,
    )
    with pytest.raises(EntityAlreadyExistsError):
        _ = service.create(user)


def test_get_all() -> None:
    resp = service.get_all()
    assert len(resp) > 0


def test_get_one(mike: PublicUser) -> None:
    resp = service.get_one(mike.name)
    assert resp == mike


def test_get_one_not_found(john: PublicUser) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = service.get_one(john.name)


def test_replace(mike: PublicUser, john: PublicUser) -> None:
    resp = service.replace(mike.name, john)
    assert resp == john


def test_replace_not_found(mike: PublicUser) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = service.replace(mike.name, mike)


def test_modify(john: PublicUser) -> None:
    john.roles = ["user", "admin"]
    resp = service.modify(john.name, PartialUser(roles=john.roles))
    assert resp == john


def test_modify_not_found(mike: PublicUser) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = service.modify(mike.name, PartialUser())


def test_delete(john: PublicUser) -> None:
    assert service.delete(john.name) is None


def test_delete_not_found(john: PublicUser) -> None:
    with pytest.raises(EntityNotFoundError):
        service.delete(john.name)
