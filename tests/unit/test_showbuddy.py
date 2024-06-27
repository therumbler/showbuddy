import unittest

from showbuddy import ShowBuddy


class TestShowBuddy(unittest.TestCase):
    def test_showbuddy(self):
        showbuddy = ShowBuddy()
        assert showbuddy is not None
        print("All tests pass")
