"""General purpose utility functions."""

from functools import partial, reduce, singledispatch, update_wrapper, wraps
import itertools as it
import operator
import os.path
import re
import string
import sys
from tempfile import TemporaryDirectory
import typing
from typing import Any, Dict, List, Sequence, Union, get_type_hints

import numpy as np
import torch


__all__ = ['copy_doc', 'format_doc', 'func_chain', 'pad_max_shape', 'remove_duplicates', 'safe_math_eval',
           'setattr_multi', 'singledispatchmethod', 'TemporaryFileName']


def autodoc(source, *, override: bool = False):
    """Automatically fill in missing docstrings from the provided source object."""

    def decorator(cls):
        def _get_func_names(obj):
            return {k for k, v in vars(obj).items() if callable(v)} - {'__init__'}

        for name in _get_func_names(cls):
            if hasattr(source, name):
                copy_doc(source, override=override)(getattr(cls, name))
        return cls

    return decorator


def copy_doc(source, *, override: bool = False):
    """Copy the docstring of one object to another."""

    def _decorator(obj):
        new = '' if (obj.__doc__ is None or override) else f'\n{obj.__doc__}'
        old = getattr(source, obj.__name__).__doc__ if isinstance(source, type) else source.__doc__
        obj.__doc__ = old + new
        return obj

    return _decorator


def format_doc(**kwargs):
    """Format the doc string of an object according to `str.format` rules."""

    def _decorator(obj):
        obj.__doc__ = obj.__doc__.format(**kwargs)
        return obj

    return _decorator


def func_chain(*funcs):
    """Return a partial object that, when called with an argument, will apply the given functions in order, using the
       output of the previous function as an input for the next (starting with the argument as the initial value).
    """
    return partial(reduce, lambda x, f: f(x), funcs)


def flatten_nested_lists(nested: List) -> List:
    """Flatten the given nested instances of lists.

    Parameters
    ----------
    nested : list
        A list possibly containing other lists.

    Returns
    -------
    flat : list
        A flat version of the given nested lists.

    Examples
    --------
    >>> flatten_nested_lists([1, 2, 3])
    [1, 2, 3]
    >>> flatten_nested_lists([1, [2, [3]]])
    [1, 2, 3]
    >>> flatten_nested_lists([1, 2, [3, [4, 5], 6], 7, 8])
    [1, 2, 3, 4, 5, 6, 7, 8]
    """
    def _flatten(obj):
        if isinstance(obj, list):
            for x in obj:
                yield from _flatten(x)
        else:
            yield obj
    return list(_flatten(nested))


def get_type_hints_with_boundary(obj, globalns=None, localns=None, boundary=None):
    """Like ``typing.get_type_hints`` for a class but allows to specify an upper boundary for the MRO."""
    if getattr(obj, '__no_type_check__', None):
        return {}
    if isinstance(obj, type):
        hints = {}
        reverse_mro = reversed(obj.__mro__)
        if boundary is not None:
            reverse_mro = it.dropwhile(lambda x: x != boundary, reverse_mro)
        for base in reverse_mro:
            if globalns is None:
                base_globals = sys.modules[base.__module__].__dict__
            else:
                base_globals = globalns
            ann = base.__dict__.get('__annotations__', {})
            for name, value in ann.items():
                if value is None:
                    value = type(None)
                if isinstance(value, str):
                    value = typing.ForwardRef(value, is_argument=False)
                value = typing._eval_type(value, base_globals, localns)
                hints[name] = value
        return hints
    return get_type_hints(obj, globalns=globalns, localns=localns)


def numpy_compatible(func):
    """Decorator which converts positional arguments from Numpy arrays to PyTorch tensors and vice versa for the return value."""
    @wraps(func)
    def _decorator(*args, **kwargs):
        use_numpy = False
        args = list(args)
        for i, arg in enumerate(args):
            if isinstance(arg, np.ndarray):
                args[i] = torch.from_numpy(arg)
                use_numpy = True
        result = func(*args, **kwargs)
        if use_numpy:
            if isinstance(result, torch.Tensor):
                result = result.numpy()
            elif isinstance(result, tuple):
                result = list(result)
                for i, res in enumerate(result):
                    if isinstance(res, torch.Tensor):
                        result[i] = res.numpy()
                result = tuple(result)
        return result
    return _decorator


def pad_max_shape(*arrays, before=None, after=1, value=0, tie_break=np.floor) -> List[np.ndarray]:
    """Pad the given arrays with a constant values such that their new shapes fit the biggest array.

    Parameters
    ----------
    arrays : sequence of arrays of the same rank
    before, after : {float, sequence, array_like}
        Similar to `np.pad -> pad_width` but specifies the fraction of values to be padded before
        and after respectively for each of the arrays.  Must be between 0 and 1.
        If `before` is given then `after` is ignored.
    value : scalar
        The pad value.
    tie_break : ufunc
        The actual number of items to be padded _before_ is computed as the total number of elements
        to be padded times the `before` fraction and the actual number of items to be padded _after_
        is the remainder. This function determines how the fractional part of the `before` pad width
        is treated. The actual `before` pad with is computed as ``tie_break(N * before).astype(int)``
        where ``N`` is the total pad width. By default `tie_break` just takes the `np.floor` (i.e.
        attributing the fraction part to the `after` pad width). The after pad width is computed as
        ``total_pad_width - before_pad_width``.

    Returns
    -------
    padded_arrays : list of arrays
    """
    shapes = np.array([x.shape for x in arrays])
    if before is not None:
        before = np.zeros_like(shapes) + before
    else:
        before = np.ones_like(shapes) - after
    max_size = shapes.max(axis=0, keepdims=True)
    margin = (max_size - shapes)
    pad_before = tie_break(margin * before.astype(float)).astype(int)
    pad_after = margin - pad_before
    pad = np.stack([pad_before, pad_after], axis=2)
    return [np.pad(x, w, mode='constant', constant_values=value) for x, w in zip(arrays, pad)]


def remove_duplicates(seq: Sequence, op=operator.eq) -> List:
    """Remove duplicates from the given sequence according to the given operator.

    Examples
    --------
    >>> import operator as op
    >>> remove_duplicates([1, 2, 3, 1, 2, 4, 1, 2, 5])
    [1, 2, 3, 4, 5]

    >>> from dataclasses import dataclass
    >>> @dataclass
    ... class Foo:
    ...     n: int
    ...
    >>> a, b, c = Foo(1), Foo(2), Foo(1)
    >>> remove_duplicates([c, b, b, c, a, b, a])
    [Foo(n=1), Foo(n=2)]
    >>> remove_duplicates([c, b, b, c, a, b, a], op=op.is_)
    [Foo(n=1), Foo(n=2), Foo(n=1)]
    """
    result = []
    duplicate_indices = set()
    for i, x in enumerate(seq):
        if i in duplicate_indices:
            continue
        result.append(x)
        for j, y in enumerate(seq[i+1:], i+1):
            if op(x, y):
                duplicate_indices.add(j)
    return result


def safe_math_eval(expr: str, locals_dict: dict = None) -> Any:
    """Safe evaluation of mathematical expressions with name resolution.

    The input string is converted to lowercase and any whitespace is removed. The expression is evaluated according
    to Python's evaluation rules (e.g. `**` denotes exponentiation). Any names, again according to Python's naming
    rules, are resolved via the `locals_dict` parameter.

    Parameters
    ----------
    expr : str
        The mathematical expression to be evaluated.
    locals_dict : dict
        Used for name resolution.

    Returns
    -------
    The value of the expression, in the context of names present in `locals_dict`.

    Raises
    ------
    TypeError
        If `expr` is not a string.
    ValueError
        If the evaluation of `expr` is considered unsafe (see the source code for exact rules).
    NameError
        If a name cannot be resolved via `locals_dict`.

    Examples
    --------
    >>> safe_math_eval('2 * 3 ** 4')
    162
    >>> import math
    >>> safe_math_eval('sqrt(2) * sin(pi/4)', {'sqrt': math.sqrt, 'sin': math.sin, 'pi': math.pi})
    1.0
    >>> safe_math_eval('2.0 * a + b', {'a': 2, 'b': 4.0})
    8.0
    """
    if not isinstance(expr, str):
        raise TypeError(f'Expression must be str not "{type(expr)}"')
    test_expr = expr.replace(' ', '').lower()
    allowed_chars = set('+-*/()_.' + string.ascii_lowercase + string.digits)  # Allow a-z for numpy or math functions.
    is_unsafe = (
        any(map(
            lambda x: x in test_expr,
            ('import', '__', '[', ']', '{', '}', 'lambda', ',', ';', ':', '"', "'")
        ))
        or not (set(test_expr) < allowed_chars)
        or any(map(
            lambda m: m is not None,
            [re.search(r'\s', test_expr),
             re.search(r'(?<![0-9])\.', test_expr),
             re.search(r'(?<![a-z])\(\)', test_expr)]
        ))
    )
    if is_unsafe:
        raise ValueError(f'Evaluation of {repr(expr)} is not safe')
    return eval(expr, {'__builtins__': {}}, locals_dict or {})


def setattr_multi(obj, names: Sequence[str], values: Union[Sequence, Dict[str, Any]]) -> None:
    """Set multiple attributes at once.

    Parameters
    ----------
    obj : object
    names : sequence
    values : sequence or dict
        If `dict` then it must map `names` to values.
    """
    if isinstance(values, dict):
        values = [values[name] for name in names]
    for name, value in zip(names, values):
        setattr(obj, name, value)


# Copy & paste from Python 3.8 functools:
# https://github.com/python/cpython/blob/0cdb21d6eb3428abe50a55f9291ca0e9728654d9/Lib/functools.py#L887
# noinspection PyUnresolvedReferences
class singledispatchmethod:
    def __init__(self, func):
        if not callable(func) and not hasattr(func, "__get__"):
            raise TypeError(f"{func!r} is not callable or a descriptor")

        self.dispatcher = singledispatch(func)
        self.func = func

    def register(self, cls, method=None):
        return self.dispatcher.register(cls, func=method)

    def __get__(self, obj, cls):
        def _method(*args, **kwargs):
            method = self.dispatcher.dispatch(args[0].__class__)
            return method.__get__(obj, cls)(*args, **kwargs)

        _method.__isabstractmethod__ = self.__isabstractmethod__
        _method.register = self.register
        update_wrapper(_method, self.func)
        return _method

    @property
    def __isabstractmethod__(self):
        return getattr(self.func, '__isabstractmethod__', False)


class TemporaryFileName(TemporaryDirectory):
    """Create a temporary file name for read and write access inside a temporary directory for portability."""

    def __init__(self, f_name: str = 'tempfile'):
        super().__init__()
        self._f_name = f_name

    def __enter__(self):
        dir_name = super().__enter__()
        return os.path.join(dir_name, self._f_name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return super().__exit__(exc_type, exc_val, exc_tb)


class PatternDict:
    """A dictionary with re.Pattern instances as keys. Item lookup is performed by matching against these patterns.

    In addition to re.Pattern, also ``str`` objects are allowed as keys when setting an item. These are converted
    internally. If such a ``str`` object contains a ``*`` it is interpreted as a wildcard and it gets converted to the
    regex equivalent: ``.*?``.
    For item lookup, only ``str`` objects are allowed since they get matched against the patterns. The first matching
    pattern's corresponding value will be returned.
    """

    def __init__(self):
        self._data = {}

    def __setitem__(self, key: Union[str, re.Pattern], value):
        if isinstance(key, str):
            key = key.replace('*', '.*?')
            key = re.compile(key)
        elif not isinstance(key, re.Pattern):
            raise TypeError(f'Keys must be one of re.Pattern or str (got {type(key)!r} instead)')
        self._data[key] = value

    def __getitem__(self, item: str):
        if not isinstance(item, str):
            raise TypeError(f'Lookup keys must str (got {type(item)!r} instead)')
        for pattern, value in self._data.items():
            if pattern.fullmatch(item):
                return value
        raise KeyError(item)

    def __contains__(self, item):
        return any(pattern.fullmatch(item) for pattern in self)

    def __iter__(self):
        return iter(self._data)

    def clear(self):
        """Remove all patterns and corresponding values."""
        self._data.clear()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
