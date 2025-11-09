import pytest

from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.user import PartialUser, PublicUser, SignInUser
from cryptid.service import user as service

from tests.common import count

key_num: int = count()

_mike: PublicUser = PublicUser(
    name=f"Mike {key_num}",
    roles=["user", "admin"],
)


@pytest.fixture
def mike() -> PublicUser:
    return _mike


@pytest.fixture
def mike_password() -> str:
    return "mike1234"


@pytest.fixture
def john() -> PublicUser:
    return PublicUser(
        id="missing",
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
    mike.id = resp.id
    mike.created_at = resp.created_at
    mike.updated_at = resp.updated_at
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
    resp = service.get_one(mike.id)
    assert resp == mike


def test_get_one_not_found(john: PublicUser) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = service.get_one(john.id)


def test_replace(mike: PublicUser, john: PublicUser) -> None:
    resp = service.replace(mike.id, john)
    mike.name = john.name
    mike.roles = john.roles
    mike.updated_at = resp.updated_at
    assert resp == mike


def test_replace_not_found(john: PublicUser) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = service.replace(john.id, john)


def test_modify(mike: PublicUser) -> None:
    mike.roles = ["user", "admin"]
    resp = service.modify(mike.id, PartialUser(roles=mike.roles))
    mike.updated_at = resp.updated_at
    assert resp == mike


def test_modify_not_found(john: PublicUser) -> None:
    with pytest.raises(EntityNotFoundError):
        _ = service.modify(john.id, PartialUser())


def test_delete(mike: PublicUser) -> None:
    assert service.delete(mike.id) is None


def test_delete_not_found(john: PublicUser) -> None:
    with pytest.raises(EntityNotFoundError):
        service.delete(john.id)
