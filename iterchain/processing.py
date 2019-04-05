import builtins
from . import chainable, Iterator


@chainable
def map(iterable, function) -> Iterator:
    """
    Applies a given function to all elements.

    Args:
        function: the function to be called on each element
    """
    return builtins.map(function, iterable)
