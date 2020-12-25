"""Even higher-order functions and operations on callable objects."""

from functools import wraps
from sys import exit    # pylint: disable=W0622
from typing import Callable, Iterable


__all__ = ['coerce', 'exiting', 'orderedfrozenset', 'wants_instance']


class orderedfrozenset(frozenset):  # pylint: disable=C0103
    """Creates a tuple with unique items."""

    def __new__(cls, items: Iterable = ()):
        ordered_items = tuple(items)
        instance = super().__new__(cls, ordered_items)
        instance._ordered_items = ordered_items
        return instance

    def __iter__(self):
        yield from self._ordered_items  # pylint: disable=E1101


def coerce(typ: type) -> Callable:
    """Converts the return value into the given type."""

    def decorator(function: Callable) -> typ:
        """Decorates the given function."""
        @wraps(function)
        def wrapper(*args, **kwargs):
            """Wraps the respective function."""
            return typ(function(*args, **kwargs))

        wrapper.__annotations__['return'] = typ
        return wrapper

    return decorator


def exiting(function: Callable) -> Callable:
    """Makes a function exit the program with its return code."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Wraps the respective function."""
        result = function(*args, **kwargs)
        exit(result or 0)

    return wrapper


def wants_instance(function: Callable) -> bool:
    """Determines whether the respective function is considered a method."""

    try:
        return function.__code__.co_varnames[0] == 'self'
    except IndexError:
        return False
