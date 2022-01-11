"""More higher-order functions and operations on callable objects."""

from functools import wraps
from sys import exit    # pylint: disable=W0622
from typing import Any, Callable, Union


__all__ = [
    'coerce',
    'exiting',
    'exitmethod',
    'instance_of',
    'wants_instance'
]


Decorator = Callable[[Callable[..., Any]], Callable[..., Any]]


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


def coerce(typ: type) -> Decorator:
    """Converts the return value into the given type."""

    def decorator(function: Callable[..., Any]) -> Callable[..., typ]:
        """Decorates the given function."""
        @wraps(function)
        def wrapper(*args, **kwargs) -> typ:
            """Wraps the respective function."""
            return typ(function(*args, **kwargs))

        wrapper.__annotations__['return'] = typ
        return wrapper

    return decorator


def exiting(function: Callable[..., Any]) -> Callable[..., Any]:
    """Makes a function exit the program with its return code."""

    @wraps(function)
    def wrapper(*args, **kwargs) -> Any:
        """Wraps the respective function."""
        result = function(*args, **kwargs)
        exit(result or 0)

    return wrapper


def instance_of(cls: Union[type, tuple[type]]) -> Callable[[Any], bool]:
    """Returns a callback function to check the instance of an object."""

    return lambda obj: isinstance(obj, cls)


def wants_instance(function: Callable[..., Any]) -> bool:
    """Determines whether the respective function is considered a method."""

    try:
        return function.__code__.co_varnames[0] == 'self'
    except IndexError:
        return False
