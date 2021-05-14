"""Even higher-order functions and operations on callable objects."""

from contextlib import suppress
from datetime import datetime
from functools import wraps
from sys import exit, stderr    # pylint: disable=W0622
from typing import Any, Callable, IO


__all__ = ['coerce', 'coroproperty', 'exiting', 'timeit', 'wants_instance']


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


def coroproperty(method: Callable) -> property:
    """Decorator for coroutine-based all-in-one getter and setter methods.

    Usage:

        class Circle:
            '''Information about a circle.'''

            def __init__(self, radius: float):
                '''Initializes the circle with its radius.'''
                self.radius = radius

            @coroproperty
            def diameter(self):
                '''Gets and sets the diameter.'''
                yield self.radius * 2
                self.radius = (yield) / 2

            @coroproperty
            def circumference(self):
                '''Gets and sets the circumference.'''
                yield self.diameter * pi
                self.diameter = (yield) / pi

            @coroproperty
            def area(self):
                '''Gets and sets the area.'''
                yield pow(self.radius, 2) * pi
                self.radius = sqrt((yield) / pi)
    """

    def getter(self) -> Any:
        """Property getter function."""
        coro = method(self)
        value = next(coro)
        coro.close()
        return value

    def setter(self, value: Any):
        """Property setter function."""
        coro = method(self)
        next(coro)
        next(coro)

        with suppress(StopIteration):
            coro.send(value)

    return property(getter, setter)


def exiting(function: Callable) -> Callable:
    """Makes a function exit the program with its return code."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Wraps the respective function."""
        result = function(*args, **kwargs)
        exit(result or 0)

    return wrapper


def timeit(file: IO = stderr) -> Callable:
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
                  file=file, flush=True)
            return result

        return wrapper

    return decorator


def wants_instance(function: Callable) -> bool:
    """Determines whether the respective function is considered a method."""

    try:
        return function.__code__.co_varnames[0] == 'self'
    except IndexError:
        return False
