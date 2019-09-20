# -*- coding: utf-8 -*-

try:
    from .context import app
except ImportError:
    from context import app

import unittest

class TestUnit(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        pass


if __name__ == '__main__':
    unittest.main()