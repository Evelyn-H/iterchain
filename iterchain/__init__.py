"""Iterator chaining for Python"""

import sys
import types

from .iterchain import Iterchain

# pylint: disable=too-few-public-methods


class IterchainModule(types.ModuleType):
    """
    Black magic to make the `iterchain` module callable.

    This means we can do this:
    ::
        >>> import iterchain
        >>> iterchain([1, 2, 3]).map(lambda x: x**2)

    instead of:
    ::

        >>> import iterchain
        >>> iterchain.Iterchain([1, 2, 3]).map(lambda x: x**2)
    """

    def __init__(self):
        super().__init__(__name__)
        self.__dict__.update(sys.modules[__name__].__dict__)

    def __call__(self, iterable):
        return Iterchain(iterable)


sys.modules[__name__] = IterchainModule()
