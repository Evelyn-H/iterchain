"""

The :code:`iterchain` module is callable, this means we can do this:
::

    >>> import iterchain
    >>> iterchain([1, 2, 3]).map(lambda x: x**2)

instead of:
::

    >>> import iterchain
    >>> iterchain.Iterator([1, 2, 3]).map(lambda x: x**2)

|

Overview
````````

**Generators**
  - :meth:`generators.count`
  - :meth:`generators.repeat`
  - ...


**Chainable operations**
  - :meth:`Iterator.map`
  - :meth:`Iterator.flat_map`
  - :meth:`Iterator.filter`
  - ...

**Reduction operators**
  - :meth:`Iterator.reduce`
  - :meth:`Iterator.all`
  - :meth:`Iterator.sum`
  - ...

**Consumers / access operators**
  - :meth:`Iterator.to_list`
  - :meth:`Iterator.first`
  - :meth:`Iterator.last`
  - ...
"""

# simplify public interface
from .core import Iterator, chainable
