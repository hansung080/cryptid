import os

from cryptid.model.explorer import Explorer, PartialExplorer

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.data import explorer as data
else:
    from cryptid.fake import explorer as data


def create(explorer: Explorer) -> Explorer:
    return data.create(explorer)


def get_all() -> list[Explorer]:
    return data.get_all()


def get_one(name: str) -> Explorer:
    return data.get_one(name)


def replace(name: str, explorer: Explorer) -> Explorer:
    return data.replace(name, explorer)


def modify(name: str, explorer: PartialExplorer) -> Explorer:
    return data.modify(name, explorer)


def delete(name: str) -> None:
    data.delete(name)
