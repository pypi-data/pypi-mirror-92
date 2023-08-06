from unittest import TestCase

from unhashlib import unhashlib

class TestUnhashlib(TestCase):
    def test(self):

        s = unhashlib("python")
        self.assertTrue(s.check("23eeeb4347bdd26bfc6b7ee9a3b755dd"))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
