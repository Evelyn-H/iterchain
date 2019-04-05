"""

"""

from . import Iterator


def count(start=0, stop=None, step=1) -> Iterator:
    """
    Makes a new iterator that returns evenly spaced values. (similar to the ``range`` builtin)

    ...
    """
    assert step is not 0
    assert stop is None or (step > 0 and stop >= start) or (step < 0 and stop <= start)

    def _count(start, stop, step):
        c = start
        while (stop is None) or (step > 0 and c < stop) or (step < 0 and c > stop):
            yield c
            c += step

    return Iterator(_count(start, stop, step))
