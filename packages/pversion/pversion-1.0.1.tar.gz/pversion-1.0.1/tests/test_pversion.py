import unittest
from pversion import get_version
from looptools import Timer


class TestPversion(unittest.TestCase):
    @Timer.decorator
    def test_pversion(self):
        ver = get_version('../pversion')

        major, minor, patch = list(int(i) for i in ver.split('.'))

        self.assertIsInstance(major, int)
        self.assertIsInstance(minor, int)
        self.assertIsInstance(patch, int)
