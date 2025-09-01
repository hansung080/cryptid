from fastapi import APIRouter, HTTPException

import cryptonamicon.service.creature as service
from cryptonamicon.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptonamicon.model.creature import Creature

router = APIRouter(prefix="/creature")


@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


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
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{name}")
@router.put("/{name}/")
def replace(name: str, creature: Creature) -> Creature:
    try:
        return service.replace(name, creature)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{name}")
@router.patch("/{name}/")
def modify(name: str, creature: Creature) -> Creature:
    try:
        return service.modify(name, creature)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{name}", status_code=204)
@router.delete("/{name}/", status_code=204)
def delete(name: str) -> None:
    try:
        service.delete(name)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
