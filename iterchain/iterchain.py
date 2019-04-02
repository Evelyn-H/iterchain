"""This is where the magic comes alive!"""


class Iterchain:
    """
    Wrapper class around python iterators

    After wrapping any iterable in this class you have access to all the chainable methods.
    These methods will also return an `Iterchain` instance to make them chainable.

    Args:
        iterable: iterable to be used. Could be a list, generator, ...

    Raises:
        ValueError: if and invalid iterable is given
    """

    def __init__(self, iterable):
        try:
            self.__iterator = iter(iterable)
        except TypeError:
            raise ValueError("You must pass a valid iterable object")

    def __iter__(self):
        return self.__iterator

    def map(self, function):
        """
        Lazily applies a function to all elements.

        Args:
            function: the function to be called on each element

        Returns:
            new Iterchain instance
        """
        return Iterchain(map(function, self))

    def to_list(self):
        """
        Converts the Iterchain to a list

        Returns:
            new list with all the elements in this Iterchain
        """
        return list(self)
