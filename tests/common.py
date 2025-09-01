import itertools

_counter = itertools.count(start=1)


def count():
    return next(_counter)
