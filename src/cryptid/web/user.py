from __future__ import annotations

import os

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from starlette import status

from cryptid.error import EntityAlreadyExistsError, EntityNotFoundError
from cryptid.model.auth import AuthUser
from cryptid.model.user import PartialUser, PublicUser, SignInUser
from cryptid.web.auth import admin_role, user_role

if not os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.service import user as service
else:
    from cryptid.fake import user as service

router: APIRouter = APIRouter(prefix="/users")


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(user: SignInUser) -> PublicUser:
    try:
        return service.create(user)
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("", dependencies=[Depends(admin_role)])
@router.get("/", dependencies=[Depends(admin_role)])
def get_all(*, deleted: bool = Query(False)) -> list[PublicUser]:
    return service.get_all(deleted=deleted)


@router.get("/me")
@router.get("/me/")
def get_me(me: AuthUser = Depends(user_role)) -> PublicUser:
    try:
        return service.get_one(me.id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{id_}", dependencies=[Depends(admin_role)])
@router.get("/{id_}/", dependencies=[Depends(admin_role)])
def get_one(id_: str, *, deleted: bool = Query(False)) -> PublicUser:
    try:
        return service.get_one(id_, deleted=deleted)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/me")
@router.put("/me/")
def replace_me(me: AuthUser = Depends(user_role), user: PublicUser = Body(...)) -> PublicUser:
    try:
        return service.replace(me.id, user)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{id_}", dependencies=[Depends(admin_role)])
@router.put("/{id_}/", dependencies=[Depends(admin_role)])
def replace(id_: str, user: PublicUser) -> PublicUser:
    try:
        return service.replace(id_, user)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.patch("/me")
@router.patch("/me/")
def modify_me(me: AuthUser = Depends(user_role), user: PartialUser = Body(...)) -> PublicUser:
    try:
        return service.modify(me.id, user)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.patch("/{id_}", dependencies=[Depends(admin_role)])
@router.patch("/{id_}/", dependencies=[Depends(admin_role)])
def modify(id_: str, user: PartialUser) -> PublicUser:
    try:
        return service.modify(id_, user)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
@router.delete("/me/", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_me(me: AuthUser = Depends(user_role)) -> None:
    try:
        service.delete(me.id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete(
    "/{id_}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    dependencies=[Depends(admin_role)],
)
@router.delete(
    "/{id_}/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    dependencies=[Depends(admin_role)],
)
def delete(id_: str) -> None:
    try:
        service.delete(id_)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
