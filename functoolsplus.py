"""Even higher-order functions and operations on callable objects."""

from time import perf_counter
from functools import wraps
from sys import exit, stderr    # pylint: disable=W0622
from typing import Any, Callable, IO, Union


__all__ = [
    'coerce',
    'exiting',
    'exitmethod',
    'instance_of',
    'timeit',
    'wants_instance'
]


class exitmethod:   # pylint: disable=C0103
    """Decorator class to create a context manager,
    having the passed function as exit method.
    """

    def __init__(self, function: Callable[..., Any]):
        self.function = function

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        if wants_instance(self.function):
            return self.function(self, typ, value, traceback)

        return self.function(typ, value, traceback)


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


def instance_of(cls: Union[type, tuple[type]]) -> Callable[[Any], bool]:
    """Returns a callback function to check the instance of an object."""

    return lambda obj: isinstance(obj, cls)


def timeit(file: IO = stderr, flush: bool = False) -> Callable:
    """Times the execution of the given function."""

    def decorator(function: Callable) -> Callable:
        """The actual decorator."""
        @wraps(function)
        def wrapper(*args, **kwargs):
            """Wraps the original function."""
            start = perf_counter()
            result = function(*args, **kwargs)
            end = perf_counter()
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
