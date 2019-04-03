Iterchain: Iterator chaining for Python
=======================================

Iterchain is a library intended to make manipulating iterators in Python easier and more ergonomic.
The functionality is based on the standard Python [itertools](https://docs.python.org/3/library/itertools.html), and the [Rust iterator design](https://doc.rust-lang.org/std/iter/index.html).



Examples
--------

Standard python:
```python
>>> list(map(lambda x: x**2, [1, 2, 3]))
[1, 4, 9]
```

With `iterchain`:
```python
>>> import iterchain
>>> iterchain([1, 2, 3]).map(lambda x: x**2).to_list()
[1, 4, 9]
```
