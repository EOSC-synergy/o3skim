"""Unittest module template."""


import unittest

from cicd import module_template


class TestCICD_module_template(unittest.TestCase):
    """Tests for `module_template` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
        self.assertTrue(module_template.hello_world())
        self.assertFalse(False)
