import unittest
from is_number.is_number import is_number


class JustTest(unittest.TestCase):


    def test_right_assert(self):
        result = is_number(20)
        self.assertEqual(result, True)
