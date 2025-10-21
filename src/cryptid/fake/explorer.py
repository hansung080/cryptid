from cryptid.fake.data import explorer as data
from cryptid.model.explorer import Explorer, PartialExplorer


def create(explorer: Explorer) -> Explorer:
    return data.create(None, explorer)


def get_all() -> list[Explorer]:
    return data.get_all(None)


def get_one(name: str) -> Explorer:
    return data.get_one(None, name)


def replace(name: str, explorer: Explorer) -> Explorer:
    return data.replace(None, name, explorer)


def modify(name: str, explorer: PartialExplorer) -> Explorer:
    return data.modify(None, name, explorer)


def delete(name: str) -> None:
    data.delete(None, name)
