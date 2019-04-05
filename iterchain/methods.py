import builtins
import functools
from . import chainable, Iterator


@chainable
def map(iterable, function) -> Iterator:
    """
    Applies a given function to all elements.

    Args:
        function: the function to be called on each element
    """
    return builtins.map(function, iterable)


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
