import os

from cryptid.data.init import get_cursor, transaction, Cursor
from cryptid.model.creature import Creature, PartialCreature

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.data import creature as data
else:
    from cryptid.fake.data import creature as data


@transaction
def create(cursor: Cursor, creature: Creature) -> Creature:
    return data.create(cursor, creature)


def get_all() -> list[Creature]:
    return data.get_all(get_cursor())


def get_one(name: str) -> Creature:
    return data.get_one(get_cursor(), name)


@transaction
def replace(cursor: Cursor, name: str, creature: Creature) -> Creature:
    return data.replace(cursor, name, creature)


@transaction
def modify(cursor: Cursor, name: str, creature: PartialCreature) -> Creature:
    return data.modify(cursor, name, creature)


@transaction
def delete(cursor: Cursor, name: str) -> None:
    data.delete(cursor, name)
