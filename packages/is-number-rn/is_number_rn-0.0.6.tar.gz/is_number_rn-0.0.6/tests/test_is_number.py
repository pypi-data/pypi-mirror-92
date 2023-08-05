import unittest
from is_number.__init__ import is_number


class JustTest(unittest.TestCase):


    def test_rright_assert(self):
        result = is_number(20)
        self.assertEqual(result, True)
