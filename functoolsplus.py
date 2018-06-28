"""Even higher-order functions and operations on callable objects."""

from collections import namedtuple
from datetime import datetime
from functools import wraps
from itertools import chain

__all__ = [
    'limit_executions',
    'once',
    'callbackpartial',
    'datetimenow',
    'returning']


Mismatch = namedtuple('Mismatch', ('arg', 'value', 'type', 'expected'))


class TypeMismatch(TypeError):
    """Indicates that one or more types did not match."""

    pass


def limit_executions(limit=1):
    """Limits the execution of a function."""

    def decorator(function):
        """Wraps the respective function."""
        executions = 0

        @wraps(function)
        def wrapper(*args, **kwargs):
            "Wraps the respective function."""
            nonlocal executions

            if executions < limit:
                executions += 1
                return function(*args, **kwargs)

            return None

        return wrapper

    return decorator


once = limit_executions(limit=1)


def callbackpartial(function, *callbacks, **kwcallbacks):
    """Returns a partial function with arguments
    extended by the results of the given callbacks.
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Wraps the respective function."""
        keywords = {name: callback() for name, callback in kwcallbacks.items()}
        keywords.update(kwargs)
        arguments = chain((callback() for callback in callbacks), args)
        return function(*arguments, **keywords)

    return wrapper


def datetimenow(function):
    """Passes datetime.now() as first
    argument to the respective function.
    """

    return callbackpartial(function, datetime.now)


def returning(type_):
    """Converts the return value into the given type."""

    def decorator(function):
        """Decorates the given function."""

        @wraps(function)
        def wrapper(*args, **kwargs):
            """Wraps the respective function."""
            return type_(function(*args, **kwargs))

        return wrapper

    return decorator


def typecheck(*types, **kwtypes):
    """Decorator factory to specify types
    expeced by the underlying function.
    """

    def decorator(function):
        """Actual decorator function."""

        @wraps(function)
        def wrapper(*args, **kwargs):
            """Wrapper function."""
            mismatches = []

            for position, (typ, arg) in enumerate(zip(types, args)):
                if typ is None:
                    continue
                elif not isinstance(arg, typ):
                    mismatches.append(Mismatch(position, arg, type(arg), typ))

            for key, value in kwargs.items():
                try:
                    typ = kwtypes[key]
                except KeyError:
                    continue

                if not isinstance(value, typ):
                    mismatches.append(Mismatch(key, value, type(value), typ))

            if mismatches:
                raise TypeMismatch(*mismatches)

            return function(*args, **kwargs)

        return wrapper

    return decorator
