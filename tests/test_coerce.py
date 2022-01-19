"""Test coerce() function."""

from typing import Any, Iterator
from unittest import TestCase

from functoolsplus import coerce


@coerce(set)
def test_coerce_set(*args, **kwargs) -> Iterator[Any]:
    for arg in args:
        yield arg

    for key, value in kwargs.items():
        yield key
        yield value


class TestCoerce(TestCase):

    def test_type_hint(self):
        self.assertEqual(test_coerce_set.__annotations__['return'], set)

    def test_return_type(self):
        self.assertIsInstance(test_coerce_set(), set)

    def test_return_value(self):
        self.assertSetEqual(
            test_coerce_set('some', 42, 'args', keyword=True, other=None),
            {'some', 42, 'args', 'keyword', True, 'other', None}
        )
