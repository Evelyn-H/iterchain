# import types
import builtins
import functools
import itertools

# from typing import Any, Callable, Generator, Iterable, TypeVar, Union
# T = TypeVar("T"); U = TypeVar("U")


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
# def returns_iterator(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         if not isinstance(result, Iterator):
#             return Iterator(result)
#         return result
#     return wrapper

def magicify(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # make sure self is an `Iterator` in case it's called as a "static" function
        if not isinstance(self, Iterator):
            self = Iterator(self)
        # make sure the output gets wrapped up as `Iterator` as well
        result = func(self, *args, **kwargs)
        if not isinstance(result, Iterator):
            result = Iterator(result)
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

    # TODO:
    # reversed
    # sorted
    # step_by
    # group_by (itertools)

    def map(self, function) -> 'Iterator':
        """
        Applies a given function to all elements.

        Args:
            function: the function to be called on each element
        """
        return Iterator(builtins.map(function, self))

    def flatten(self) -> 'Iterator':
        return Iterator(itertools.chain.from_iterable(self))

    def flat_map(self, function) -> 'Iterator':
        return self.map(function).flatten()

    def star_map(self, function) -> 'Iterator':
        return Iterator(itertools.starmap(function, self))

    def filter(self, function) -> 'Iterator':
        return Iterator(builtins.filter(function, self))

    def filter_false(self, predicate=None) -> 'Iterator':
        return Iterator(itertools.filterfalse(predicate, self))

    def enumerate(self, start=0) -> 'Iterator':
        return Iterator(builtins.enumerate(self, start))

    def slice(self, *args) -> 'Iterator':
        return Iterator(itertools.islice(self, *args))

    def take(self, n) -> 'Iterator':
        return self.slice(0, n)

    def take_while(self, predicate) -> 'Iterator':
        return Iterator(itertools.takewhile(predicate, self))

    def skip(self, n) -> 'Iterator':
        # FIXME: kind of a sloppy implementation
        def _skip(iterable, n):
            for _ in range(n):
                try:
                    next(self)
                except StopIteration:
                    return
            for i in iterable:
                yield i
        return Iterator(_skip(self, n))

    def drop(self, n) -> 'Iterator':
        return self.skip(n)

    def skip_while(self, predicate) -> 'Iterator':
        return Iterator(itertools.dropwhile(predicate, self))

    def drop_while(self, predicate) -> 'Iterator':
        return self.skip_while(predicate)

    def inspect(self, function) -> 'Iterator':
        # FIXME: kind of a sloppy implementation
        def _inspect(iterator, function):
            for i in iterator:
                function(i)
                yield i
        return Iterator(_inspect(self, function))

    def chain(self, *iterables) -> 'Iterator':
        return Iterator(itertools.chain(self, *iterables))

    def compress(self, selectors) -> 'Iterator':
        return Iterator(itertools.compress(self, selectors))

    def product(self, *iterables, repeat=1) -> 'Iterator':
        return Iterator(itertools.product(self, *iterables, repeat=repeat))

    def permutations(self, r=None) -> 'Iterator':
        return Iterator(itertools.permutations(self, r=r))

    def combinations(self, r) -> 'Iterator':
        return Iterator(itertools.combinations(self, r))

    def combinations_with_replacement(self, r) -> 'Iterator':
        return Iterator(itertools.combinations_with_replacement(self, r))

    def cycle(self) -> 'Iterator':
        return Iterator(itertools.cycle(self))


    # ==== TERMINATORS (Iterator -> object) ====

    # TODO:
    # all
    # any
    # min, max
    # sum
    # product # conflicts with the cartesian/set product
    # length

    # first
    # last
    # nth
    # for_each
    # partition
    # find / position'

    def reduce(self, initial, function):
        return functools.reduce(function, self, initial)

    def next(self):
        return next(self)

    def collect(self, constructor=None):
        if constructor:
            return constructor(self)
        else:
            # just use up the iterator but don't do anything with it
            # could be useful if you somehow have side effects
            # you wanna execute but don't need the results
            for _ in self:
                pass
            return None

    def to_list(self) -> list:
        """
        Converts the Iterchain to a list

        Returns:
            new list containing all the elements in this Iterchain
        """
        return self.collect(list)


    # ==== Generators (new Iterator) ====

    # TODO:
    # successors (rust)
    # zip (normal, strict, longest) / unzip

    @classmethod
    def range(cls, *args) -> 'Iterator':
        """
        Makes a new iterator that returns evenly spaced values. 
        (similar to the ``range`` builtin)
        """
        return Iterator(range(*args))

    @classmethod
    def count(cls, start=0, step=1) -> 'Iterator':
        return Iterator(itertools.count(start, step))

    @classmethod
    def repeat(cls, item, times=None) -> "Iterator":
        if times:
            return Iterator(itertools.repeat(item, times))
        else:
            return Iterator(itertools.repeat(item))
