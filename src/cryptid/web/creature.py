import os

from fastapi import APIRouter, HTTPException
from starlette import status

from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.creature import Creature, PartialCreature

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.service import creature as service
else:
    from cryptid.fake import creature as service

router = APIRouter(prefix="/creatures")


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
@router.get("/{name}/")
def get_one(name: str) -> Creature:
    try:
        return service.get_one(name)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{name}")
@router.put("/{name}/")
def replace(name: str, creature: Creature) -> Creature:
    try:
        return service.replace(name, creature)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{name}")
@router.patch("/{name}/")
def modify(name: str, creature: PartialCreature) -> Creature:
    try:
        return service.modify(name, creature)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/{name}/", status_code=status.HTTP_204_NO_CONTENT)
def delete(name: str) -> None:
    try:
        service.delete(name)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
