# -*- coding: utf-8 -*-

try:
    from .context import app
except ImportError:
    from context import app

import unittest

class TestIntegration(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        pass


if __name__ == '__main__':
    unittest.main()
