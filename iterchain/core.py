# import sys
# import types
import functools
import builtins

# # # to implement:

# # generators
# count / range
# repeat
# successors (rust)
# cycle
# zip / unzip
# chain
# next

# # chainable
# map
# flat_map
# flatten
# filter
# take
# skip
# enumerate
# reversed
# sorted
# step_by
# inspect

# # consuming / non-chainable
# reduce
# all
# any
# min, max
# sum
# product

# first
# last
# nth
# for_each
# to_list / collect
# partition
# find / position'

def chainable(func=None, *, returns_iterable=True):
    """
    Decorator that allows you to add your own custom chainable methods.

    The wrapped function should take the an :class:`Iterator` instance as the first argument,
    and should return an iterable object (does not have to be an :class:`Iterator` instance).

    The original function is not modified and can still be used as normal.

    Args:
        returns_iterable (bool): whether or not the wrapped function returns an iterable

    Example:
    ::

        >>> @iterchain.chainable
        >>> def plus(iterable, amount):
        ...     return iterable.map(lambda x: x + amount)
        ...
        >>> iterchain([1, 2, 3]).plus(1).to_list()
        [2, 3, 4]

    """
    def _chainable(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if returns_iterable and not isinstance(result, Iterator):
                return Iterator(result)
            return result

        if hasattr(Iterator, func.__name__):
            raise AttributeError("Chainable method {} already exists.".format(func.__name__))
        setattr(Iterator, func.__name__, wrapper)
        return func

    # to allow the decorator to be used with and without arguments
    if func is None:
        return _chainable
    return _chainable(func)


# simple QoL decorator to avoid repeated code.
# all it does is wrap the return value into an Iterator instance if it isn't one already
def _returns_iterator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if not isinstance(result, Iterator):
            return Iterator(result)
        return result
    return wrapper


class Iterator():
    """
    Wrapper class around python iterators

    After wrapping any iterable in this class it will have access to all the methods listed below.
    These methods also return an `Iterator` instance to make them chainable.

    ``<3``
    """

    # ==== BASICS ====

    # TODO: duplicate the `sentinel` behaviour of the builtin
    # (don't actually have to program it, just copy the args to builtins.iter(...))
    def __init__(self, iterable):
        try:
            self._iterator = builtins.iter(iterable)
        except TypeError:
            raise ValueError("You must pass a valid iterable object")

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iterator)

    # ==== TRANSFORMATIONS (Iterator -> Iterator) ====

    @_returns_iterator
    def map(self, function) -> 'Iterator':
        """
        Applies a given function to all elements.

        Args:
            function: the function to be called on each element
        """
        return builtins.map(function, self)


    # ==== TERMINATORS (Iterator -> object) ====

    def reduce(self, initial, function):
        return functools.reduce(function, self, initial)

    def to_list(self) -> list:
        """
        Converts the Iterchain to a list

        Returns:
            new list containing all the elements in this Iterchain
        """
        return list(self)


    # ==== Generators (new Iterator) ====

    @classmethod
    def count(cls, start=0, stop=None, step=1) -> 'Iterator':
        """
        Makes a new iterator that returns evenly spaced values. (similar to the ``range`` builtin)

        ...
        """
        assert step != 0
        assert stop is None or (step > 0 and stop >= start) or (step < 0 and stop <= start)

        def _count(start, stop, step):
            counter = start
            while (stop is None) or (step > 0 and counter < stop) or (step < 0 and counter > stop):
                yield counter
                counter += step

        return Iterator(_count(start, stop, step))
