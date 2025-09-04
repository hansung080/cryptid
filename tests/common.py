import itertools

_counter = itertools.count(start=1)


def count() -> int:
    return next(_counter)
