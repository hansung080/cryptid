from _pytest._code.code import ExceptionInfo
from fastapi import HTTPException
from starlette import status


def assert_already_exists_error(error: ExceptionInfo[HTTPException]) -> None:
    assert error.value.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in error.value.detail


def assert_not_found_error(error: ExceptionInfo[HTTPException]) -> None:
    assert error.value.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in error.value.detail
