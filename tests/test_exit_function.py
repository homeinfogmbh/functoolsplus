"""Test exit_function() decorator."""

from unittest import TestCase

from functoolsplus import exit_function


@exit_function
def test_function(typ, value, traceback):
    if typ is None and value is None:
        return True

    if issubclass(typ, Exception) and isinstance(value, Exception):
        return True


class TestExitFunction(TestCase):
    """Test exit_function()."""

    def test_type(self):
        self.assertIsInstance(test_function, exit_function)

    def test_is_context_manager(self):
        self.assertTrue(hasattr(test_function, '__enter__'))
        self.assertTrue(hasattr(test_function, '__exit__'))

    def test_context(self):
        with test_function as manager:
            self.assertIsInstance(manager, exit_function)
            self.assertTrue(hasattr(manager, '__exit__'))

    def test_exception_handling(self):
        with test_function:
            raise Exception()
