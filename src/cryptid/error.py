class EntityAlreadyExistsError(Exception):
    def __init__(self, entity: str, key: str) -> None:
        self.entity = entity
        self.key = key

    def __str__(self):
        return f"{self.entity} '{self.key}' already exists"


class EntityNotFoundError(Exception):
    def __init__(self, entity: str, key: str) -> None:
        self.entity = entity
        self.key = key

    def __str__(self):
        return f"{self.entity} '{self.key}' not found"
