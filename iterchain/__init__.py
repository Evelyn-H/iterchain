"""

The :code:`iterchain` module is callable, this means we can do this:
::

    >>> import iterchain
    >>> iterchain([1, 2, 3]).map(lambda x: x**2)

instead of:
::

    >>> import iterchain
    >>> iterchain.Iterchain([1, 2, 3]).map(lambda x: x**2)
"""


import sys
import types
import typing

class Iterchain:
    """
    Wrapper class around python iterators

    After wrapping any iterable in this class it will have access to all the methods listed below.
    These methods also return an `Iterchain` instance to make them chainable.

    ``<3``
    """

    def __init__(self, iterable):
        try:
            self.__iterator = iter(iterable)
        except TypeError:
            raise ValueError("You must pass a valid iterable object")

    def __iter__(self):
        return self.__iterator

    def map(self, function) -> 'Iterchain':
        """
        Lazily applies a function to all elements.

        Args:
            function: the function to be called on each element
        """
        return Iterchain(map(function, self))

    def to_list(self) -> list:
        """
        Converts the Iterchain to a list

        Returns:
            new list containing all the elements in this Iterchain
        """
        return list(self)


# pylint: disable=too-few-public-methods
class IterchainModule(types.ModuleType):
    """
    Black magic to make the ``iterchain`` module callable.
    """

    def __init__(self):
        super().__init__(__name__)
        self.__dict__.update(sys.modules[__name__].__dict__)

    def __call__(self, iterable):
        return Iterchain(iterable)


sys.modules[__name__] = IterchainModule()
