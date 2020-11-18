"""Even higher-order functions and operations on callable objects."""

from functools import wraps
from sys import exit    # pylint: disable=W0622
from typing import Callable, Iterable


__all__ = ['coerce', 'exiting', 'orderedfrozenset', 'wants_instance']


def coerce(typ: type) -> Callable:
    """Converts the return value into the given type."""

    def decorator(function: Callable) -> typ:
        """Decorates the given function."""

        @wraps(function)
        def wrapper(*args, **kwargs):
            """Wraps the respective function."""
            return typ(function(*args, **kwargs))

        return wrapper

    return decorator


def exiting(function: Callable) -> Callable:
    """Makes a function exit the program with its return code."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Wraps the respective function."""
        result = function(*args, **kwargs)

        if result is None:
            exit(0)

        exit(result)

    return wrapper


@coerce(tuple)
def orderedfrozenset(items: Iterable = ()):
    """Creates a tuple with unique items."""

    processed = set()

    for item in items:
        if item not in processed:
            processed.add(item)
            yield item


def wants_instance(function: Callable) -> bool:
    """Determines whether the respective function is considered a method."""

    try:
        return function.__code__.co_varnames[0] == 'self'
    except IndexError:
        return False
