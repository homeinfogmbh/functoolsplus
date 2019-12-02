"""Even higher-order functions and operations on callable objects."""

from functools import wraps


__all__ = ['coerce', 'orderedfrozenset', 'wants_instance']


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


@coerce(tuple)
def orderedfrozenset(items=()):
    """Creates a tuple with unique items."""

    processed = set()

    for item in items:
        if item not in processed:
            processed.add(item)
            yield item


def wants_instance(function):
    """Determines whether the respective function is considered a method."""

    try:
        return function.__code__.co_varnames[0] == 'self'
    except IndexError:
        return False
