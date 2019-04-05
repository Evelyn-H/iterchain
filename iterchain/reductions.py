import functools

from . import chainable


@chainable(returns_iterable=False)
def reduce(iterable, initial, function):
    return functools.reduce(function, iterable, initial)


@chainable(returns_iterable=False)
def to_list(iterable) -> list:
    """
    Converts the Iterchain to a list

    Returns:
        new list containing all the elements in this Iterchain
    """
    return list(iterable)
