"""Test exit_method() decorator."""

from unittest import TestCase

from functoolsplus import exit_method


@exit_method
def test_method(self, typ, value, traceback):
    if typ is None and value is None:
        return True

    if issubclass(typ, Exception) and isinstance(value, Exception):
        return True


class TestExitMethod(TestCase):
    """Test exit_method()."""

    def test_is_context_manager(self):
        self.assertTrue(hasattr(test_method, '__enter__'))
        self.assertTrue(hasattr(test_method, '__exit__'))

    def test_context(self):
        with test_method as manager:
            self.assertIsInstance(manager, test_method)

    def test_exception_handling(self):
        with test_method:
            raise Exception()