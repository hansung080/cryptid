import os

from fastapi import APIRouter, HTTPException
from starlette import status

from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.explorer import Explorer, PartialExplorer

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.service import explorer as service
else:
    from cryptid.fake import explorer as service

router = APIRouter(prefix="/explorer")


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(explorer: Explorer) -> Explorer:
    try:
        return service.create(explorer)
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{name}")
@router.get("/{name}/")
def get_one(name: str) -> Explorer:
    try:
        return service.get_one(name)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{name}")
@router.put("/{name}/")
def replace(name: str, explorer: Explorer) -> Explorer:
    try:
        return service.replace(name, explorer)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{name}")
@router.patch("/{name}/")
def modify(name: str, explorer: PartialExplorer) -> Explorer:
    try:
        return service.modify(name, explorer)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/{name}/", status_code=status.HTTP_204_NO_CONTENT)
def delete(name: str) -> None:
    try:
        service.delete(name)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
