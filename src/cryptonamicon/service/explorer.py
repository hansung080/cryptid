import cryptonamicon.fake.explorer as data

from cryptonamicon.model.explorer import Explorer


def create(explorer: Explorer) -> Explorer:
    return data.create(explorer)


def get_all() -> list[Explorer]:
    return data.get_all()


def get_one(name: str) -> Explorer | None:
    return data.get_one(name)


def replace(name: str, explorer: Explorer) -> Explorer | None:
    return data.replace(name, explorer)


def modify(name: str, explorer: Explorer) -> Explorer | None:
    return data.modify(name, explorer)


def delete(name: str) -> bool:
    return data.delete(name)
