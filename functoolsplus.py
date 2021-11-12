"""Even higher-order functions and operations on callable objects."""

from datetime import datetime
from functools import wraps
from sys import exit, stderr    # pylint: disable=W0622
from typing import Any, Callable, IO


__all__ = ['coerce', 'exiting', 'wants_instance']


def coerce(typ: type) -> Callable[..., Any]:
    """Converts the return value into the given type."""

    def decorator(function: Callable) -> Callable[..., typ]:
        """Decorates the given function."""
        @wraps(function)
        def wrapper(*args, **kwargs) -> typ:
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


def timeit(file: IO = stderr, flush: bool = False) -> Callable:
    """Times the execution of the given function."""

    def decorator(function: Callable) -> Callable:
        """The actual decorator."""
        @wraps(function)
        def wrapper(*args, **kwargs):
            """Wraps the original function."""
            start = datetime.now()
            result = function(*args, **kwargs)
            end = datetime.now()
            print('Function', function.__name__, 'took', end - start,
                  file=file, flush=flush)
            return result

        return wrapper

    return decorator


def wants_instance(function: Callable) -> bool:
    """Determines whether the respective function is considered a method."""

    try:
        return function.__code__.co_varnames[0] == 'self'
    except IndexError:
        return False
