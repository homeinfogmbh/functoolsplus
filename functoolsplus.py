"""Even higher-order functions and operations on callable objects."""

from functools import wraps


__all__ = ['cached_method', 'coerce', 'wants_instance']


def cached_method(attr='cache'):
    """Caches the return value of the
    function within an instance attribute.
    """

    def decorator(method):
        """Actual decorator."""

        @wraps(method)
        def wrapper(instance, *args, **kwargs):
            """Wraps the respective method."""
            cache = getattr(instance, attr)

            try:
                return cache[method]
            except KeyError:
                result = method(instance, *args, **kwargs)
                cache[method] = result
                return result

        return wrapper

    return decorator


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
