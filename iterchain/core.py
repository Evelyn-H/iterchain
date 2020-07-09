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


class Iterator:
    """
    Wrapper class around python iterators

    After wrapping any iterable in this class it will have access to all the methods listed below.
    These methods also return an `Iterator` instance to make them chainable.

    ``<3``
    """

    def __init__(self, iterable):
        try:
            self.__iterator = builtins.iter(iterable)
        except TypeError:
            raise ValueError("You must pass a valid iterable object")

    def __iter__(self):
        return self.__iterator

    def __next__(self):
        return next(self.__iterator)


# simple wrapper function around the Iterator constructor to mimic the builtins.iter behaviour.
# TODO: duplicate the `sentinel` behaviour of the builtin
def iter(iterable): # pylint: disable=redefined-builtin
    return Iterator(iterable)


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
            if returns_iterable:
                return Iterator(func(self, *args, **kwargs))
            return func(self, *args, **kwargs)

        if hasattr(Iterator, func.__name__):
            raise AttributeError("Chainable method {} already exists.".format(func.__name__))
        setattr(Iterator, func.__name__, wrapper)
        return func

    # to allow the decorator to be used with and without arguments
    if func is None:
        return _chainable
    return _chainable(func)


# class _IterchainModule(types.ModuleType):
#     """
#     Black magic to make the ``iterchain`` module callable.
#     """

#     def __init__(self):
#         super().__init__(__name__)
#         self.__dict__.update(sys.modules[__name__].__dict__)

#     def __call__(self, iterable):
#         return Iterator(iterable)

# and change this module to our patched version
# sys.modules[__name__] = _IterchainModule()
