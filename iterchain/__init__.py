"""

The :code:`iterchain` module is callable, this means we can do this:
::

    >>> import iterchain
    >>> iterchain([1, 2, 3]).map(lambda x: x**2)

instead of:
::

    >>> import iterchain
    >>> iterchain.Iterator([1, 2, 3]).map(lambda x: x**2)
"""


import sys
import types

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
# last
# nth
# for_each
# to_list / collect
# partition
# find / position'


# predefine to make the typechecker happy
class Iterator:
    pass


class Iterator:
    """
    Wrapper class around python iterators

    After wrapping any iterable in this class it will have access to all the methods listed below.
    These methods also return an `Iterator` instance to make them chainable.

    ``<3``
    """

    def __init__(self, iterable):
        try:
            self.__iterator = iter(iterable)
        except TypeError:
            raise ValueError("You must pass a valid iterable object")

    def __iter__(self):
        return self.__iterator

    def __next__(self):
        return next(self.__iterator)

    def map(self, function) -> Iterator:
        """
        Lazily applies a function to all elements.

        Args:
            function: the function to be called on each element
        """
        return Iterator(map(function, self))

    def to_list(self) -> list:
        """
        Converts the Iterchain to a list

        Returns:
            :obj:`list`: new list containing all the elements in this Iterchain
        """
        return list(self)


# pylint: disable=too-few-public-methods
class _IterchainModule(types.ModuleType):
    """
    Black magic to make the ``iterchain`` module callable.
    """

    def __init__(self):
        super().__init__(__name__)
        self.__dict__.update(sys.modules[__name__].__dict__)


    def __call__(self, iterable):
        return Iterator(iterable)


# import at the end to avoid cyclic imports
from .generators import *

# and change this module to our patched version
sys.modules[__name__] = _IterchainModule()
