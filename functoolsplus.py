"""More higher-order functions and operations on callable objects."""

from functools import partial, wraps
from typing import Any, Callable, Union


__all__ = ['coerce', 'exit_function', 'exit_method', 'instance_of']


class exit_function:
    """Decorator class to create a context manager,
    having the passed function as exit function.
    """

    __slots__ = ('function',)

    def __init__(self, function: Callable[..., Any]):
        self.function = function

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        return self.function(typ, value, traceback)


def exit_method(method: Callable[..., Any]):
    """Decorator class to create a context manager,
    having the passed function as exit method.
    """

    class ContextManager:
        __slots__ = ()

        def __enter__(self):
            return self

        __exit__ = method

    return ContextManager()


def coerce(typ: type) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
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


def instance_of(cls: Union[type, tuple[type]]) -> Callable[[Any], bool]:
    """Returns a callback function to check the instance of an object."""

    return lambda obj: isinstance(obj, cls)
