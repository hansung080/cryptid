import os

from cryptid.data.init import get_conn
from cryptid.model.creature import Creature, PartialCreature

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.data import creature as data
else:
    from cryptid.fake.data import creature as data

_conn = get_conn()
_cursor = _conn.cursor()


def create(creature: Creature) -> Creature:
    return data.create(_cursor, creature)


def get_all() -> list[Creature]:
    return data.get_all(_cursor)


def get_one(name: str) -> Creature:
    return data.get_one(_cursor, name)


def replace(name: str, creature: Creature) -> Creature:
    return data.replace(_cursor, name, creature)


def modify(name: str, creature: PartialCreature) -> Creature:
    return data.modify(_cursor, name, creature)


def delete(name: str) -> None:
    data.delete(_cursor, name)
