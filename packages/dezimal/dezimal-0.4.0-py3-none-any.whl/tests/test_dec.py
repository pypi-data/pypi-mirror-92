import unittest
from numbers import Number

from dezimal import Dezimal

from apm import *


class DecTest(unittest.TestCase):

    def test_construct_from_int(self):
        self.assertEqual("194", str(Dezimal(194)))
        self.assertEqual("-194", str(Dezimal(-194)))

    def test_construct_from_str(self):
        self.assertEqual("1", str(Dezimal("1")))
        self.assertEqual("1", str(Dezimal("1.0")))
        self.assertEqual("1.01", str(Dezimal("1.01")))
        self.assertEqual("1", str(Dezimal("+1")))
        self.assertEqual("1", str(Dezimal("+1.0")))
        self.assertEqual("1.01", str(Dezimal("+1.01")))
        self.assertEqual("-1", str(Dezimal("-1")))
        self.assertEqual("-1", str(Dezimal("-1.0")))
        self.assertEqual("-1.01", str(Dezimal("-1.01")))
        self.assertEqual("0", str(Dezimal("0")))
        self.assertEqual("0", str(Dezimal("0.0")))
        self.assertEqual("0.01", str(Dezimal("0.01")))
        self.assertEqual("0", str(Dezimal("+0")))
        self.assertEqual("0", str(Dezimal("+0.0")))
        self.assertEqual("0.01", str(Dezimal("+0.01")))
        self.assertEqual("0", str(Dezimal("-0")))
        self.assertEqual("0", str(Dezimal("-0.0")))
        self.assertEqual("-0.01", str(Dezimal("-0.01")))

    def test_construct_from_str_scifi_notation(self):
        self.assertEqual("1", str(Dezimal("1e0")))
        self.assertEqual("1", str(Dezimal("1e+0")))
        self.assertEqual("1", str(Dezimal("1e-0")))
        self.assertEqual("-1", str(Dezimal("-1e0")))
        self.assertEqual("-1", str(Dezimal("-1e+0")))
        self.assertEqual("-1", str(Dezimal("-1e-0")))
        self.assertEqual("1", str(Dezimal("1.0e0")))
        self.assertEqual("1", str(Dezimal("1.0e+0")))
        self.assertEqual("1", str(Dezimal("1.0e-0")))
        self.assertEqual("-1", str(Dezimal("-1.0e0")))
        self.assertEqual("-1", str(Dezimal("-1.0e+0")))
        self.assertEqual("-1", str(Dezimal("-1.0e-0")))

        self.assertEqual("10", str(Dezimal("1e1")))
        self.assertEqual("10", str(Dezimal("1e+1")))
        self.assertEqual("0.1", str(Dezimal("1e-1")))
        self.assertEqual("-10", str(Dezimal("-1e1")))
        self.assertEqual("-10", str(Dezimal("-1e+1")))
        self.assertEqual("-0.1", str(Dezimal("-1e-1")))
        self.assertEqual("10", str(Dezimal("1.0e1")))
        self.assertEqual("10", str(Dezimal("1.0e+1")))
        self.assertEqual("0.1", str(Dezimal("1.0e-1")))
        self.assertEqual("-10", str(Dezimal("-1.0e1")))
        self.assertEqual("-10", str(Dezimal("-1.0e+1")))
        self.assertEqual("-0.1", str(Dezimal("-1.0e-1")))

    def test_add(self):
        self.assertEqual(Dezimal("103.03"), Dezimal("100") + Dezimal("3.03"))

    def test_sub(self):
        self.assertEqual(Dezimal("96.97"), Dezimal("100") - Dezimal("3.03"))

    def test_mul(self):
        self.assertEqual(Dezimal("1.26"), Dezimal("1.2") * Dezimal("1.05"))

    def test_div(self):
        self.assertEqual("0.33333333333333333", str(Dezimal(1) / Dezimal(3)))

    def test_add_different_types(self):
        self.assertEqual(Dezimal(6), Dezimal(3) + 3)
        self.assertEqual(Dezimal(6), 3 + Dezimal(3))

    def test_matches(self):
        self.assertTrue(match(Dezimal(1), Dezimal(1)))
        self.assertTrue(match(Dezimal(1), Strict(Dezimal(1))))
        self.assertTrue(match(Dezimal(1), Dezimal(1), strict=True))

    def test_instanceof_number(self):
        self.assertTrue(match(Dezimal(1), InstanceOf(Number)))


if __name__ == '__main__':
    unittest.main()
