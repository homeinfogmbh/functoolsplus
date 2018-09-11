"""Even higher-order functions and operations on callable objects."""

from datetime import datetime
from functools import wraps
from itertools import chain

__all__ = [
    'callbackpartial',
    'datetimenow',
    'coerce',
    'wants_instance']


def callbackpartial(function, *callbacks, **kwcallbacks):
    """Returns a partial function with arguments
    extended by the results of the given callbacks.
    Keyword arguments explicitely passed to the resulting
    function may override keywords derived from callbacks.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Wraps the respective function."""
        keywords = {name: callback() for name, callback in kwcallbacks.items()}
        # Allow passed kwargs to override callback kwargs.
        keywords.update(kwargs)
        arguments = chain((callback() for callback in callbacks), args)
        return function(*arguments, **keywords)

    return wrapper


def datetimenow(function):
    """Passes datetime.now() as first
    argument to the respective function.
    """

    return callbackpartial(function, datetime.now)


def coerce(type_):
    """Converts the return value into the given type."""

    def decorator(function):
        """Decorates the given function."""

        @wraps(function)
        def wrapper(*args, **kwargs):
            """Wraps the respective function."""
            return type_(function(*args, **kwargs))

        return wrapper

    return decorator


def wants_instance(function):
    """Determines whether the respective function is considered a method."""

    args = function.__code__.co_varnames[:function.__code__.co_argcount]

    try:
        return args[0] == 'self'
    except IndexError:
        return False
