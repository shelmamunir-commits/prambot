import unittest
from datetime import date

from utils import validasi as v


class TestValidasi(unittest.TestCase):
    def test_nama(self):
        self.assertTrue(v.valid_nama("Rina Putri"))
        self.assertFalse(v.valid_nama(""))
        self.assertFalse(v.valid_nama("R1na"))
        self.assertFalse(v.valid_nama(123))

    def test_tanggal(self):
        self.assertTrue(v.valid_tanggal(date(2000, 1, 1)))
        self.assertFalse(v.valid_tanggal(date(1800, 1, 1)))
        self.assertFalse(v.valid_tanggal("2000-01-01"))

    def test_parse_tanggal(self):
        self.assertEqual(v.parse_tanggal("17-08-1945"), date(1945, 8, 17))
        self.assertEqual(v.parse_tanggal("1945-08-17"), date(1945, 8, 17))
        with self.assertRaises(ValueError):
            v.parse_tanggal("kemarin")


if __name__ == "__main__":
    unittest.main()
