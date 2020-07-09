from iterchain.core import Iterator as iter # pylint: disable=redefined-builtin


def test():
    l = [1, 2, 3]
    new_l = (iter(l)
             .map(lambda x: x**2)
             .to_list())

    assert new_l == [1, 4, 9]

    assert iter.count(start=2, step=-1, stop=-2).to_list() == [2, 1, 0, -1]
