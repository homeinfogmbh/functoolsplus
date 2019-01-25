"""Even higher-order functions and operations on callable objects."""

from functools import wraps


__all__ = ['cached_method', 'coerce', 'orderedfrozenset', 'wants_instance']


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
            result = function(*args, **kwargs)
            return type_(result)

        return wrapper

    return decorator


def orderedfrozenset(items=None):
    """Creates a tuple with unique items."""

    if items is None:
        return ()

    processed = set()
    elements = []

    for item in items:
        if item in processed:
            continue

        processed.add(item)
        elements.append(item)

    return tuple(elements)


def wants_instance(function):
    """Determines whether the respective function is considered a method."""

    args = function.__code__.co_varnames[:function.__code__.co_argcount]

    try:
        return args[0] == 'self'
    except IndexError:
        return False
