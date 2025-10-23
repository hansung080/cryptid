import os

from cryptid.data.init import get_cursor, transaction, Cursor
from cryptid.model.explorer import Explorer, PartialExplorer

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.data import explorer as data
else:
    from cryptid.fake.data import explorer as data


@transaction
def create(cursor: Cursor, explorer: Explorer) -> Explorer:
    return data.create(cursor, explorer)


def get_all() -> list[Explorer]:
    return data.get_all(get_cursor())


def get_one(name: str) -> Explorer:
    return data.get_one(get_cursor(), name)


@transaction
def replace(cursor: Cursor, name: str, explorer: Explorer) -> Explorer:
    return data.replace(cursor, name, explorer)


@transaction
def modify(cursor: Cursor, name: str, explorer: PartialExplorer) -> Explorer:
    return data.modify(cursor, name, explorer)


@transaction
def delete(cursor: Cursor, name: str) -> None:
    data.delete(cursor, name)
