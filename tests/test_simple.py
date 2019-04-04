import iterchain


def test():
    l = [1, 2, 3]
    new_l = (iterchain(l)
        .map(lambda x: x**2)
        .to_list())

    assert new_l == [1, 4, 9]

    assert iterchain.count(start=2, step=-1, stop=-2).to_list() == [2, 1, 0, -1]
