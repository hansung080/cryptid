from cryptid.fake.data import user as data
from cryptid.model.user import PublicUser, SignInUser, PrivateUser, PartialUser
from cryptid.service.auth import make_hash


def create(user: SignInUser) -> PublicUser:
    private_user = PrivateUser(
        name=user.name,
        roles=user.roles,
        hash=make_hash(user.password),
    )
    return data.create(None, private_user)


def get_all(*, deleted: bool = False) -> list[PublicUser]:
    if deleted:
        raise NotImplementedError("function 'get_all' with argument 'deleted=True' not implemented")
    return data.get_all(None)


def get_one(id_: str, *, deleted: bool = False) -> PublicUser:
    if deleted:
        raise NotImplementedError("function 'get_one' with argument 'deleted=True' not implemented")
    return data.get_one(None, id_)


def replace(id_: str, user: PublicUser) -> PublicUser:
    return data.replace(None, id_, user)


def modify(id_: str, user: PartialUser) -> PublicUser:
    return data.modify(None, id_, user)


def delete(id_: str) -> None:
    data.delete(None, id_)
