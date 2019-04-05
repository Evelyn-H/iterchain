"""

"""

from . import Iterator


def count(start=0, stop=None, step=1) -> Iterator:
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
