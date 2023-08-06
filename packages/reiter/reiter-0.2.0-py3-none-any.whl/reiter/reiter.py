"""Random-access interface for iterables.

Wrapper for Python iterators and iterables that implements a list-like
random-access interface by caching retrieved items for later reuse.
"""

from __future__ import annotations
import doctest
from collections.abc import Iterator

class reiter(Iterator): # pylint: disable=C0103
    """
    Wrapper class for iterators and iterables.
    """

    _iterated = None
    _iterable = None
    _complete = None

    def __new__(cls, iterable):
        """
        Constructor that wraps an iterator or iterable.

        >>> xs = iter([1, 2, 3])
        >>> isinstance(reiter(xs), reiter)
        True
        >>> list(reiter(reiter(iter([1, 2, 3]))))
        [1, 2, 3]
        >>> reiter(123)
        Traceback (most recent call last):
          ...
        TypeError: supplied object is not iterable
        """
        if isinstance(iterable, reiter):
            return iterable

        if not isinstance(iterable, Iterator):
            try:
                iterable = iter(iterable)
            except TypeError:
                raise TypeError('supplied object is not iterable') from None

        instance = super().__new__(cls)
        instance._iterable = iter(iterable)
        instance._iterated = []
        instance._complete = False
        return instance

    def __next__(self):
        """
        Substitute definition that caches the retrieved
        item before returning it.

        >>> xs = reiter([1, 2, 3])
        >>> [x for x in xs]
        [1, 2, 3]
        >>> xs = reiter(iter([1, 2, 3]))
        >>> [x for x in xs]
        [1, 2, 3]
        >>> xs = reiter(iter([1, 2, 3]))
        >>> next(xs)
        1
        """
        item = self._iterable.__next__()
        self._iterated.append(item)
        return item

    def __getitem__(self, index):
        """
        Returns the item at the specified index, retrieving
        additional items from the iterator (and caching them)
        as necessary to reach the specified index.

        >>> xs = reiter([1, 2, 3])
        >>> xs[2]
        3
        >>> xs = reiter(range(10))
        >>> xs[0]
        0
        >>> xs = reiter(range(10))
        >>> xs[10]
        Traceback (most recent call last):
          ...
        IndexError: index out of range
        """
        if len(self._iterated) <= index:
            for _ in range(len(self._iterated), index + 1):
                try:
                    item = next(self._iterable)
                    self._iterated.append(item)
                except StopIteration:
                    self._complete = True

        if index >= len(self._iterated):
            raise IndexError('index out of range')

        return self._iterated[index] # pylint: disable=E1136

    def __iter__(self):
        """
        Build a new iterator that begins at the first cached
        element and continues from there. This method
        is an effective way to "reset" the iterator.

        >>> xs = reiter([1, 2, 3])
        >>> next(xs)
        1
        >>> next(xs)
        2
        >>> list(reiter(xs))
        [1, 2, 3]
        >>> next(xs)
        Traceback (most recent call last):
          ...
        StopIteration
        >>> list(reiter(xs))
        [1, 2, 3]
        >>> list(reiter(xs))
        [1, 2, 3]
        """
        for item in self._iterated: # pylint: disable=E1133
            yield item
        while True:
            try:
                item = self._iterable.__next__()
                self._iterated.append(item)
                yield item
            except StopIteration:
                self._complete = True
                break

    def has(self, index=None):
        """
        Return a boolean indicating whether a next item is available,
        or if an item exists at the specified index.

        >>> xs = reiter([1, 2, 3])
        >>> (xs.has(), xs.has(2), xs.has())
        (True, True, False)
        >>> xs = reiter([1, 2, 3])
        >>> xs.has(10)
        False
        """
        index = len(self._iterated) if index is None else index
        try:
            self[index] # pylint: disable=W0104
            return True
        except (StopIteration, IndexError):
            return False

    def length(self):
        """
        If all items have been retrieved, return the length.

        >>> xs = reiter([1, 2, 3])
        >>> xs.length() is None
        True
        >>> list(xs)
        [1, 2, 3]
        >>> xs.length()
        3
        """
        if self._complete:
            return len(self._iterated)

        # If not all items have been retrieved from the iterable,
        # there is not yet a defined length.
        return None

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
