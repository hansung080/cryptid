import os

from cryptid.data.init import get_conn
from cryptid.model.explorer import Explorer, PartialExplorer

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.data import explorer as data
else:
    from cryptid.fake.data import explorer as data

_conn = get_conn()
_cursor = _conn.cursor()


def create(explorer: Explorer) -> Explorer:
    return data.create(_cursor, explorer)


def get_all() -> list[Explorer]:
    return data.get_all(_cursor)


def get_one(name: str) -> Explorer:
    return data.get_one(_cursor, name)


def replace(name: str, explorer: Explorer) -> Explorer:
    return data.replace(_cursor, name, explorer)


def modify(name: str, explorer: PartialExplorer) -> Explorer:
    return data.modify(_cursor, name, explorer)


def delete(name: str) -> None:
    data.delete(_cursor, name)
