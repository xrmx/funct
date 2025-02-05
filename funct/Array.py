import itertools
import math
import multiprocessing
import operator
import warnings
from collections.abc import Iterable, Sequence
from concurrent.futures import ThreadPoolExecutor
from functools import reduce


class Array(list):
    """
    A functional mutable sequence
    inheriting from the built-in list.
    """

    __baseIterables = (list, range, tuple)

    def __init__(self, *args):

        """
        Constructs an Array from arguments.
        Nested lists, tuples and range objects are converted to
        Arrays, while other iterables will stored as Array elements.
        """
        if len(args) == 1 and isinstance(args[0], Iterable):
            args = list(args[0])

        if any(map(lambda e: isinstance(e, Array.__baseIterables), args)):
            super().__init__(self.__convert(a) for a in args)
        else:
            super().__init__(args)

    def add(self, e):
        """
        Element-wise addition with given scalar or sequence.
        """
        return self.__operate(operator.add, e)

    def add_(self, e):
        """
        Inplace element-wise addition with given scalar or sequence.
        """
        self[:] = self.__operate(operator.add, e)
        return self

    def sub(self, e):
        """
        Element-wise subtraction with given scalar or sequence.
        """
        return self.__operate(operator.sub, e)

    def sub_(self, e):
        """
        Inplace element-wise subtraction with given scalar or sequence.
        """
        self[:] = self.__operate(operator.sub, e)
        return self

    def mul(self, e):
        """
        Element-wise multiplication with given scalar or sequence.
        """
        return self.__operate(operator.mul, e)

    def mul_(self, e):
        """
        Inplace element-wise multiplication with given scalar or sequence.
        """
        self[:] = self.__operate(operator.mul, e)
        return self

    def div(self, e):
        """
        Element-wise division with given scalar or sequence.
        """
        return self.__operate(operator.truediv, e)

    def div_(self, e):
        """
        Inplace element-wise division with given scalar or sequence.
        """
        self[:] = self.__operate(operator.truediv, e)
        return self

    def pow(self, e):
        """
        Raises elements of this Array to given power,
        or sequence of powers, element-wise.
        """
        return self.__operate(operator.pow, e)

    def pow_(self, e):
        """
        Raises elements (in-place) of this Array to given power,
        or sequence of powers, element-wise.
        """
        self[:] = self.__operate(operator.pow, e)
        return self

    def mod(self, e):
        """
        Computes the remainder between elements in this Array
        and given scalar or sequence, element-wise.
        """
        return self.__operate(operator.mod, e)

    def mod_(self, e):
        """
        Computes (in-place) the remainder between elements in this Array
        and given scalar or sequence, element-wise.
        """
        self[:] = self.__operate(operator.mod, e)
        return self

    def bitwiseAnd(self, e):
        """
        Computes the bit-wise AND between elements in this Array
        and given scalar or sequence, element-wise.
        """
        return self & e

    def bitwiseAnd_(self, e):
        """
        Computes (in-place) the bit-wise AND between elements in this Array
        and given scalar or sequence, element-wise.
        """
        self[:] = self & e
        return self

    def bitwiseOr(self, e):
        """
        Computes the bit-wise OR between elements in this Array
        and given scalar or sequence, element-wise.
        """
        return self | e

    def bitwiseOr_(self, e):
        """
        Computes (in-place) the bit-wise OR between elements in this Array
        and given scalar or sequence, element-wise.
        """
        self[:] = self | e
        return self

    def abs(self):
        """ Element-wise absolute value. """
        return Array(map(abs, self))

    def abs_(self):
        """ Inplace element-wise absolute value. """
        self[:] = self.abs()
        return self

    def sum(self):
        """ Returns the sum of the Array elements. """
        return sum(self)

    def product(self):
        """ Returns the product of the Array elements. """
        return reduce(lambda a, b: a * b, self)

    def mean(self):
        """ Returns the average of the Array elements. """
        return sum(self) / self.size

    def average(self, weights=None):
        """ Returns the weighted average of the Array elements. """
        if weights is None:
            return sum(self) / self.size
        else:
            return sum(self.mul(weights)) / sum(weights)

    def floor(self):
        """ Floors the Array elements. """
        return Array(map(math.floor, self))

    def floor_(self):
        """ Floors the Array elements in-place. """
        self[:] = Array(map(math.floor, self))
        return self

    def ceil(self):
        """ Ceils the Array elements. """
        return Array(map(math.ceil, self))

    def ceil_(self):
        """ Ceils the Array elements in-place. """
        self[:] = Array(map(math.ceil, self))
        return self

    def round(self, d=0):
        """ Rounds the Array to the given number of decimals. """
        return Array(map(lambda e: round(e, d), self))

    def round_(self, d=0):
        """ Rounds the Array in-place to the given number of decimals. """
        self[:] = Array(map(lambda e: round(e, d), self))
        return self

    def gt(self, e):
        """ Returns x > y element-wise """
        return self.__gt__(e)

    def gt_(self, e):
        """ Returns x > y element-wise (in-place) """
        self[:] = self.__gt__(e)
        return self

    def ge(self, e):
        """ Returns x >= y element-wise """
        return self.__ge__(e)

    def ge_(self, e):
        """ Returns x >= y element-wise (in-place) """
        self[:] = self.__ge__(e)
        return self

    def lt(self, e):
        """ Returns x < y element-wise """
        return self.__lt__(e)

    def lt_(self, e):
        """ Returns x < y element-wise (in-place) """
        self[:] = self.__lt__(e)
        return self

    def le(self, e):
        """ Returns x <= y element-wise """
        return self.__le__(e)

    def le_(self, e):
        """ Returns x <= y element-wise (in-place) """
        self[:] = self.__le__(e)
        return self

    def eq(self, e):
        """ Returns x == y element-wise """
        return self.__eq__(e)

    def eq_(self, e):
        """ Returns x == y element-wise (in-place) """
        self[:] = self.__eq__(e)
        return self

    def ne(self, e):
        """ Returns x != y element-wise """
        return self.__ne__(e)

    def ne_(self, e):
        """ Returns x != y element-wise (in-place) """
        self[:] = self.__ne__(e)
        return self

    def accumulate(self, l=operator.add):
        """
        Returns accumulated Array of elements using provided function.
        Defaults to accumulated sum.
        """
        return Array(itertools.accumulate(self, l))

    def clip(self, _min, _max):
        """
        Clip the values in the Array between the interval (`_min`, `_max`).
        """
        return Array(map(lambda e: max(min(e, _max), _min), self))

    def clip_(self, _min, _max):
        """ Clip the values in the Array in-place. """
        self[:] = Array(map(lambda e: max(min(e, _max), _min), self))
        return self

    def roll(self, n):
        """ Rolls the elements of the Array. """
        n = n % self.size
        return self[-n:] + self[:-n]

    def roll_(self, n):
        """ Rolls the elements of the Array in-place. """
        n = n % self.size
        self[:] = self[-n:] + self[:-n]
        return self

    def cat(self, b):
        """ Concatenates a sequence to this Array. """
        return self + Array(b)

    def diff(self, n=1):
        """ Returns the n-th discrete difference of the Array. """
        if n == 1:
            return self[1:].sub(self[:-1])
        else:
            return self[1:].sub(self[:-1]).diff(n - 1)

    def difference(self, b):
        """
        Difference between this Array and another iterable.
        Returns the values in this Array that are not in sequence b.
        """
        s = set(b)
        return Array(e for e in self if e not in s)

    def setDifference(self, b):
        """
        Difference between this Array and another iterable.
        Returns the unique values in this Array that are not in sequence b.
        Does not preserve order of elements.
        """
        return Array(set(self).difference(set(b)))

    def intersect(self, b):
        """
        Intersection between this Array and another iterable.
        Returns the values that are both in this Array and sequence b.
        """
        s = set(b)
        return Array(e for e in self if e in s)

    def setIntersect(self, b):
        """
        Intersection between this Array and another iterable.
        Returns the unique values that are both in this Array and sequence b.
        Does not preserve order of elements.
        """
        return Array(set(self).intersection(set(b)))

    def union(self, b):
        """
        Union of this Array and another iterable.
        Returns the values that are in either this Array or sequence b.
        """
        return self + b

    def setUnion(self, b):
        """
        Union of this Array and another iterable.
        Returns the unique values that are in either this Array or sequence b.
        Does not preserve order of elements.
        """
        return Array(set(self).union(set(b)))

    def unique(self):
        """
        Selects unique values in this Array.
        Does not preserve order of elements.
        """
        return Array(set(self))

    def nunique(self):
        """ Returns the number of unique elements in the Array. """
        return len(set(self))

    def equal(self, b):
        """ Returns true this Array and given sequence have the same elements. """
        self.__validate_seq(b)
        return all(self.eq(b))

    def remove(self, b):
        """ Removes first occurence(s) of the value(s). """
        a = self.copy()
        if isinstance(b, Iterable):
            for i in b:
                super(Array, a).remove(i)
        else:
            super(Array, a).remove(b)
        return a

    def remove_(self, b):
        """ Removes first occurence(s) of the value(s) in-place. """
        if isinstance(b, Iterable):
            for i in b:
                super().remove(i)
        else:
            super().remove(b)
        return self

    def removeByIndex(self, b):
        """ Removes the value at specified index or indices. """
        a = self.copy()
        if isinstance(b, Iterable):
            try:
                c = 0
                for i in b:
                    a.pop(i - c)
                    c += 1
            except TypeError:
                raise TypeError(
                    "{} object cannot be interpreted as an integer".format(
                        type(i).__name__
                    )
                ) from None
        else:
            try:
                a.pop(b)
            except TypeError:
                raise TypeError(
                    "{} object cannot be interpreted as an integer".format(
                        type(b).__name__
                    )
                ) from None
        return a

    def removeByIndex_(self, b):
        """ Removes the value at specified index or indices in-place. """
        if isinstance(b, Iterable):
            try:
                c = 0
                for i in b:
                    self.pop(i - c)
                    c += 1
            except TypeError:
                raise TypeError(
                    "{} object cannot be interpreted as an integer".format(
                        type(i).__name__
                    )
                ) from None
        else:
            try:
                self.pop(b)
            except TypeError:
                raise TypeError(
                    "{} object cannot be interpreted as an integer".format(
                        type(b).__name__
                    )
                ) from None
        return self

    def get(self, key, default=None):
        """
        Safe method for getting elements in the Array.
        Returns default if the index does not exist.
        """
        try:
            return self[key]
        except IndexError:
            return default

    def map(self, l):
        """
        Returns an Array by applying provided function to all elements of this Array.
        """
        return Array(map(l, self))

    def starmap(self, l):
        """
        Returns an Array by applying provided function
        to this Array with itertools.starmap
        """
        return Array(itertools.starmap(l, self))

    def parmap(self, fun, processes=None):
        """
        Returns an Array by applying a function to
        all elements of this Array in parallel.
        """
        with multiprocessing.Pool(processes=processes) as pool:
            return Array(pool.map(fun, self))

    def parstarmap(self, fun, processes=None):
        """ Parallel starmap """
        with multiprocessing.Pool(processes=processes) as pool:
            return Array(pool.starmap(fun, self))

    def asyncmap(self, fun, max_workers=None):
        """
        Executes map asynchronously.
        Returns a Future object.
        """
        executor = ThreadPoolExecutor(max_workers=max_workers)
        try:
            return executor.submit(self.map, fun)
        finally:
            executor.shutdown(wait=False)

    def asyncstarmap(self, fun, max_workers=None):
        """
        Executes starmap asynchronously.
        Returns a Future object.
        """
        executor = ThreadPoolExecutor(max_workers=max_workers)
        try:
            return executor.submit(self.starmap, fun)
        finally:
            executor.shutdown(wait=False)

    def filter(self, l):
        """ Selects elements of this Array which satisfy the predicate. """
        return Array(filter(l, self))

    def forall(self, l):
        """
        Returns whether the specified predicate
        holds for all elements of this Array.
        """
        return all(map(l, self))

    def forany(self, l):
        """
        Returns whether the specified predicate
        holds for any element of this Array.
        """
        return any(map(l, self))

    def reduce(self, l, init=None):
        """ Reduces the elements of this Array using the specified operator. """
        if init is not None:
            return reduce(l, self, init)
        return reduce(l, self)

    def contains(self, e):
        """ Tests wheter element exists in this Array. """
        return e in self

    def indexWhere(self, l):
        """ Finds the index of the first element satisfying a predicate. """
        for i, v in enumerate(self):
            if l(v):
                return i
        raise ValueError("No matches")

    def indicesWhere(self, l):
        """ Finds all the indices of the elements satisfying a predicate. """
        return Array(i for i, v in enumerate(self) if l(v))

    def indices(self, e):
        """ Returns all the indices of provided value in this Array. """
        r = []
        o = -1
        while True:
            try:
                o = self.index(e, o + 1)
            except ValueError:
                return Array(r)
            r.append(o)

    def split(self, c):
        """
        Splits an Array into subarrays using provided argument as the delimiter element.
        """
        try:
            i = self.index(c)
            v = self[:i].unsqueeze if i != 0 else Array()
            for e in self[i + 1 :].split(c):
                if len(e) != 0:
                    v.append(e)
            return v
        except ValueError:
            return self.unsqueeze

    def splitTo(self, n):
        """ Splits this Array to n equal length subarrays """
        if self.size % n != 0:
            raise ValueError("Split does not result in an equal division")
        d = self.size // n
        return Array(self[d * i : d * (i + 1)] for i in range(n))

    def splitAt(self, n):
        """ Splits this Array into subarrays at specified index or indices. """
        if isinstance(n, int):
            return Array(self[:n], self[n:])
        n = Array(0, *n, self.size)
        return Array(self[n[i] : n[i + 1]] for i in range(n.size - 1))

    def takeWhile(self, l):
        """ Takes the longest prefix of elements that satisfy the given predicate. """
        return Array(itertools.takewhile(l, self))

    def dropWhile(self, l):
        """ Drops the longest prefix of elements that satisfy the given predicate. """
        return Array(itertools.dropwhile(l, self))

    def groupBy(self, l):
        """
        Groups this Array into an Array of Array-tuples according
        to given discriminator function.
        """
        m = {}
        for v in self:
            k = l(v)
            if k in m:
                m[k].append(v)
            else:
                m[k] = Array([v])
        return Array(m.items())

    def maxBy(self, l):
        """ Finds the maximum value measured by a function. """
        return max(self, key=l)

    def minBy(self, l):
        """ Finds the minimum value measured by a function. """
        return min(self, key=l)

    def sortBy(self, l, reverse=False):
        """
        Sorts this Array according to a function
        defining the sorting criteria.
        """
        return Array(sorted(self, key=l, reverse=reverse))

    def sortBy_(self, l, reverse=False):
        """
        Sorts this Array in place according to a function
        defining the sorting criteria.
        """
        super().sort(key=l, reverse=reverse)
        return self

    def argsortBy(self, l, reverse=False):
        """
        Returns the indices that would sort this Array according to
        provided sorting criteria.
        """
        return self.enumerate.sortBy(lambda e: l(e[1]), reverse=reverse)[:, 0]

    def sort(self, **kwargs):
        """ Sorts this Array. """
        return Array(sorted(self, **kwargs))

    def sort_(self, **kwargs):
        """ Sorts this Array in place. """
        super().sort(**kwargs)
        return self

    def argsort(self, reverse=False):
        """ Returns the indices that would sort this Array """
        return self.enumerate.sortBy(lambda e: e[1], reverse=reverse)[:, 0]

    def reverse(self):
        """ Reverses this Array. """
        return Array(reversed(self))

    def reverse_(self):
        """ Reverses this Array in-place. """
        super().reverse()
        return self

    def copy(self):
        return Array(super().copy())

    def asType(self, t):
        """
        Converts the elements in this Array to given type.
        """
        return Array(map(t, self))

    def join(self, delimiter=" "):
        """
        Creates a string representation of this Array
        with elements separated with `delimiter`
        """
        return delimiter.join(str(v) for v in self)

    def append(self, e):
        """
        Appends an element to the end of this Array.
        """
        super().append(self.__convert(e))
        return self

    def prepend(self, e):
        """
        Prepends an element to the beginning of this Array.
        """
        super().insert(0, self.__convert(e))
        return self

    def extend(self, e):
        """ Extend this Array by appending elements from the iterable. """
        super().extend(Array(e))
        return self

    def extendLeft(self, e):
        """ Extends this Array by prepending elements from the iterable. """
        self[0:0] = Array(e)
        return self

    def insert(self, i, e):
        """ Inserts element(s) (in place) before given index/indices. """
        if isinstance(e, Array.__baseIterables) and isinstance(
            i, Array.__baseIterables
        ):
            if len(e) != len(i):
                raise ValueError(
                    "The lengths of the sequences must match, got {} and {}".format(
                        len(i), len(e)
                    )
                )
            for ii, ei in zip(i, e):
                self.insert(ii, ei)
        else:
            super().insert(i, self.__convert(e))
        return self

    def fill(self, e):
        """ Replaces all elements of this Array with given object. """
        return Array([e] * self.size)

    def fill_(self, e):
        """ Replaces (in place) all elements of this Array with given object. """
        self[:] = e
        return self

    def pad(self, n, value=0):
        """ Pads this Array with value. """
        try:
            return self + [value] * n
        except TypeError:
            raise TypeError(
                "{} object cannot be interpreted as an integer".format(type(n).__name__)
            ) from None

    def padLeft(self, n, value=0):
        """ Pads this Array with value. """
        try:
            return [value] * n + self
        except TypeError:
            raise TypeError(
                "{} object cannot be interpreted as an integer".format(type(n).__name__)
            ) from None

    def padTo(self, n, value=0):
        """
        Pads this Array with value until length of n is reached.
        """
        try:
            return self + [value] * (n - self.size)
        except TypeError:
            raise TypeError(
                "{} object cannot be interpreted as an integer".format(type(n).__name__)
            ) from None

    def padLeftTo(self, n, value=0):
        """ Pads this Array with value until length of n is reached. """
        try:
            return [value] * (n - self.size) + self
        except TypeError:
            raise TypeError(
                "{} object cannot be interpreted as an integer".format(type(n).__name__)
            ) from None

    def zip(self, *args):
        return Array(zip(self, *args))

    def unzip(self):
        """
        'Unzips' nested Arrays by unpacking its elements into a zip.

        >>> Array((1, "a"), (2, "b")).unzip()
        Array(Array(1, 2), Array('a', 'b'))
        """
        if not all(map(lambda e: isinstance(e, Iterable), self)):
            raise TypeError("Array elements must support iteration")
        return Array(zip(*self))

    def zipAll(self, *args, default=None):
        """
        Zips the sequences. If the iterables are
        of uneven length, missing values are filled with default value.
        """
        return Array(itertools.zip_longest(self, *args, fillvalue=default))

    @property
    def all(self):
        """ Returns true if bool(e) is True for all elements in this Array. """
        return all(self)

    @property
    def any(self):
        """ Returns true if bool(e) is True for any element e in this Array. """
        return any(self)

    @property
    def max(self):
        return max(self)

    @property
    def argmax(self):
        """ Returns the index of the maximum value """
        return self.enumerate.maxBy(lambda e: e[1])[0]

    @property
    def min(self):
        return min(self)

    @property
    def argmin(self):
        """ Returns the index of the minimum value """
        return self.enumerate.minBy(lambda e: e[1])[0]

    @property
    def head(self):
        """ Selects the first element of this Array. """
        return self[0]

    @property
    def headOption(self, default=None):
        """
        Selects the first element of this Array if it has one,
        otherwise returns default.
        """
        return self.get(0, default)

    @property
    def last(self):
        """ Selects the last element of this Array. """
        return self[-1]

    @property
    def lastOption(self, default=None):
        """
        Selects the last element of this Array if it has one,
        otherwise returns default.
        """
        return self.get(-1, default)

    @property
    def init(self):
        """ Selects the rest of this Array without its last element. """
        return self[:-1]

    @property
    def tail(self):
        """ Selects the rest of this Array without its first element. """
        return self[1:]

    @property
    def isEmpty(self):
        """ Returns whether this Array is empty. """
        return self.size == 0

    @property
    def nonEmpty(self):
        """ Returns whether this Array is not empty. """
        return self.size != 0

    @property
    def isFinite(self):
        """
        Returns True if none of the elements are neither infinity nor NaN.
        """
        return all(map(math.isfinite, self))

    @property
    def length(self):
        """ Number of elements in this Array. """
        return self.__len__()

    @property
    def size(self):
        """ Number of elements in this Array. """
        return self.__len__()

    @property
    def toInt(self):
        """ Converts elements in this Array to integers. """
        try:
            return Array(map(lambda e: ord(e) if isinstance(e, str) else int(e), self))
        except TypeError:
            raise TypeError("Expected an Array of numbers or characters") from None

    @property
    def toBool(self):
        """ Converts elements in this Array to booleans. """
        return Array(map(bool, self))

    @property
    def toArray(self):
        """ Converts all iterables in the Array to Arrays """
        return Array(
            map(lambda e: Array(e).toArray if isinstance(e, Iterable) else e, self)
        )

    @property
    def toChar(self):
        """ Converts an Array of integers to chars. """
        return Array(map(chr, self))

    @property
    def toStr(self):
        """
        Creates a string representation of the Array.
        See Array.join for more functionality.
        """
        return "".join(str(v) for v in self)

    @property
    def toTuple(self):
        """ Returns a copy of the Array as an tuple. """
        return tuple(self.copy())

    @property
    def toSet(self):
        """ Returns set of the Array elements. Order is not preserved. """
        return set(self)

    @property
    def toIter(self):
        """ Returns an iterator for the Array."""
        for e in self:
            yield e

    @property
    def toDict(self):
        """ Creates a dictionary from an Array of Arrays / tuples. """
        return dict(self)

    @property
    def squeeze(self):
        """
        Returns the Array with the same elements, but with
        outermost singleton dimension removed (if exists).
        """
        if isinstance(self.headOption, Array.__baseIterables) and self.length == 1:
            return self[0]
        else:
            return self

    @property
    def unsqueeze(self):
        """
        Returns the Array with the same elements wrapped in a Array.
        """
        return Array([self])

    @property
    def flatten(self):
        """ Returns the Array collapsed into one dimension. """
        r = Array(e for s in self for e in (s if isinstance(s, Iterable) else [s]))
        if any(map(lambda e: isinstance(e, Iterable), r)):
            return r.flatten
        return r

    @property
    def range(self):
        """ Returns the indices of the Array"""
        return Array(range(self.size))

    @property
    def enumerate(self):
        """ Zips the Array with its indices """
        return Array(enumerate(self))

    @staticmethod
    def zeros(n):
        """ Returns a zero-filled Array of given length. """
        try:
            return Array([0] * n)
        except TypeError:
            raise TypeError(
                "{} object cannot be interpreted as an integer".format(type(n).__name__)
            ) from None

    @staticmethod
    def arange(*args):
        """
        Returns an Array of evenly spaced values within given interval

        Parameters
        ----------
        start: number, optional
        end: number
        step: number, optional
        """
        _len = len(args)
        if _len == 0:
            raise TypeError("Expected at least one argument")
        elif _len > 3:
            raise TypeError("Expected at most 3 arguments")
        elif _len == 1:
            return Array(range(math.ceil(args[0])))
        start, end, step = args if _len == 3 else args + (1,)
        return Array(start + step * i for i in range(math.ceil((end - start) / step)))

    @staticmethod
    def linspace(start, stop, num=50, endpoint=True):
        """
        Returns evenly spaced Array over a specified interval.

        Parameters
        ----------
        start: number
        stop: number
        num: int, optional
        endpoint : bool, optional
        """
        step = (stop - start) / max(num - bool(endpoint), 1)
        return Array(start + step * i for i in range(num))

    @staticmethod
    def logspace(start, stop, num=50, base=10, endpoint=True):
        """
        Returns Array spaced evenly on a log scale.

        Parameters
        ----------
        start: number
        stop: number
        num: int, optional
        base: float, optional
        endpoint: bool, optional
        """
        return base ** Array.linspace(start, stop, num, endpoint)

    def __convert(self, e):
        return Array(e) if isinstance(e, Array.__baseIterables) else e

    def __validate_seq(self, e):
        if len(e) != self.size:
            raise ValueError(
                "The lengths of the sequences must match, got {} and {}".format(
                    self.size, len(e)
                )
            )

    def __validate_index(self, i):
        if not isinstance(i, (int, slice)):
            if not isinstance(i, Sequence) or not all(
                map(lambda e: isinstance(e, (bool, int, slice)), i)
            ):
                raise TypeError(
                    "Only integers, slices and 1d integer or boolean Arrays are valid indices"
                )

    def __validate_setelem(self, i, e):
        if isinstance(e, Iterable):
            if len(i) != len(e):
                raise ValueError(
                    "Expected Array of size {}, got {}".format(len(i), len(e))
                )
            return iter(e)
        else:
            return itertools.repeat(e)

    def __operate(self, f, e):
        if isinstance(e, Iterable):
            self.__validate_seq(e)
            return Array(map(f, self, e))
        return Array(map(f, self, itertools.repeat(e)))

    def __repr__(self):
        return "Array" + "(" + super().__repr__()[1:-1] + ")"

    def __add__(self, b):
        if isinstance(b, Array.__baseIterables):
            return Array(super().__add__(Array(b)))
        else:
            raise TypeError(f"Can not concatenate {type(b).__name__} to Array")

    def __iadd__(self, b):
        if isinstance(b, Array.__baseIterables):
            super().__iadd__(b)
            return self
        else:
            raise TypeError(f"Can not concatenate {type(b).__name__} to Array")

    def __radd__(self, b):
        if isinstance(b, Array.__baseIterables):
            return Array(b) + self
        else:
            raise TypeError(f"Can not concatenate {type(b).__name__} to Array")

    def __rpow__(self, b):
        if isinstance(b, Array.__baseIterables):
            self.__validate_seq(b)
            return Array(b).pow(self)
        return Array([b] * self.size).pow(self)

    def __gt__(self, e):
        return self.__operate(operator.gt, e)

    def __ge__(self, e):
        return self.__operate(operator.ge, e)

    def __lt__(self, e):
        return self.__operate(operator.lt, e)

    def __le__(self, e):
        return self.__operate(operator.le, e)

    def __eq__(self, e):
        return self.__operate(operator.eq, e)

    def __ne__(self, e):
        return self.__operate(operator.ne, e)

    def __and__(self, e):
        return self.__operate(operator.and_, e)

    def __or__(self, e):
        return self.__operate(operator.or_, e)

    def __neg__(self):
        return Array(map(operator.neg, self))

    def __invert__(self):
        if all(map(lambda e: isinstance(e, bool), self)):
            return Array(map(lambda e: not e, self))
        return Array(map(operator.inv, self))

    def __hash__(self):
        return hash(self.toTuple)

    def __bool__(self):
        if self.__len__() == 0:
            warnings.warn(
                "The truth value of an empty Array is ambiguous. Use `Array.nonEmpty` to check that Array is not empty",
                UserWarning,
            )
        return all(self)

    def __setitem__(self, key, e):
        self.__validate_index(key)
        if isinstance(key, tuple):
            if len(key) == 1:
                key = key[0]
            else:
                if isinstance(key[0], int):
                    self[key[0]][key[1:]] = e
                    return
                try:
                    idx = range(*key[0].indices(self.size))
                    for ic in idx:
                        self[ic][key[1:]]
                    for ic, ie in zip(idx, self.__validate_setelem(idx, e)):
                        self[ic][key[1:]] = ie
                except TypeError:
                    raise IndexError("Too many indices for the Array") from None
                return
        if isinstance(key, int):
            super().__setitem__(key, self.__convert(e))
            return
        if isinstance(key, Sequence):
            for _i, _e in zip(key, self.__validate_setelem(key, e)):
                super().__setitem__(_i, _e)
            return
        if isinstance(e, Iterable):
            e = self.__convert(e)
        else:
            e = [e] * len(range(*key.indices(self.size)))
        super().__setitem__(key, e)

    def __getitem__(self, key):
        self.__validate_index(key)
        if isinstance(key, tuple):
            if len(key) == 1:
                key = key[0]
            else:
                if isinstance(key[0], int):
                    return self[key[0]][key[1:]]
                try:
                    return Array(e[key[1:]] for e in super().__getitem__(key[0]))
                except TypeError:
                    raise IndexError("Too many indices for the Array") from None
        if isinstance(key, int):
            return super().__getitem__(key)
        if isinstance(key, slice):
            return Array(super().__getitem__(key))
        if all(map(lambda k: isinstance(k, bool), key)):
            if len(key) != self.size:
                raise IndexError(
                    "Expected boolean Array of size {}, got {}".format(
                        self.size, len(key)
                    )
                )
            key = (i for i, k in enumerate(key) if k)
        return Array(map(super().__getitem__, key))
