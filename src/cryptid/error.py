from __future__ import annotations


class EntityAlreadyExistsError(Exception):
    def __init__(self, entity: str, key: str) -> None:
        self.entity = entity
        self.key = key

    def __str__(self) -> str:
        return f"{self.entity} '{self.key}' already exists"


class EntityNotFoundError(Exception):
    def __init__(self, entity: str, key: str) -> None:
        self.entity = entity
        self.key = key

    def __str__(self) -> str:
        return f"{self.entity} '{self.key}' not found"


class AuthenticationError(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class JWTValidationError(AuthenticationError):
    def __init__(self, msg: str = "") -> None:
        super().__init__(msg)

    def __str__(self) -> str:
        if self.msg:
            return self.msg
        elif self.__cause__:
            return str(self.__cause__)
        else:
            return "jwt validation error"
