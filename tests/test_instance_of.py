"""Test instance_of() function."""

from unittest import TestCase

from functoolsplus import instance_of


ITEMS = ("string", 42, "other string", 3.14, 1337, True, False, None)


class TestInstanceOf(TestCase):
    def test_filter_str(self):
        self.assertSequenceEqual(
            list(filter(instance_of(str), ITEMS)), ["string", "other string"]
        )

    def test_filter_int(self):
        self.assertSequenceEqual(
            list(filter(instance_of(int), ITEMS)), [42, 1337, 1, 0]
        )

    def test_filter_float(self):
        self.assertSequenceEqual(list(filter(instance_of(float), ITEMS)), [3.14])

    def test_filter_bool(self):
        self.assertSequenceEqual(list(filter(instance_of(bool), ITEMS)), [True, False])

    def test_map_str(self):
        self.assertSequenceEqual(
            list(map(instance_of(str), ITEMS)),
            [True, False, True, False, False, False, False, False],
        )

    def test_map_int(self):
        self.assertSequenceEqual(
            list(map(instance_of(int), ITEMS)),
            [False, True, False, False, True, True, True, False],
        )

    def test_map_float(self):
        self.assertSequenceEqual(
            list(map(instance_of(float), ITEMS)),
            [False, False, False, True, False, False, False, False],
        )

    def test_map_bool(self):
        self.assertSequenceEqual(
            list(map(instance_of(bool), ITEMS)),
            [False, False, False, False, False, True, True, False],
        )
