import unittest
from datetime import date

from utils import validasi as v


class TestValidasi(unittest.TestCase):
    def test_nama(self):
        self.assertTrue(v.valid_nama("Rina"))
        self.assertTrue(v.valid_nama("Dr. R.A. Kartini"))
        with self.assertRaises(ValueError):
            v.valid_nama("")
        with self.assertRaises(ValueError):
            v.valid_nama("   ")
        with self.assertRaises(ValueError):
            v.valid_nama("Rina123")
        with self.assertRaises(TypeError):
            v.valid_nama(123)

    def test_tanggal(self):
        self.assertTrue(v.valid_tanggal(date(2000, 1, 1)))
        with self.assertRaises(ValueError):
            v.valid_tanggal(date(1800, 1, 1))
        with self.assertRaises(ValueError):
            v.valid_tanggal(date(2150, 1, 1))
        with self.assertRaises(TypeError):
            v.valid_tanggal("2000-01-01")

    def test_hari_dan_pasaran(self):
        self.assertTrue(v.valid_hari("Senin"))
        self.assertTrue(v.valid_pasaran("Kliwon"))
        with self.assertRaises(KeyError):
            v.valid_hari("Funday")
        with self.assertRaises(KeyError):
            v.valid_pasaran("PahingX")

    def test_parse_tanggal(self):
        self.assertEqual(v.parse_tanggal("17-08-1945"), date(1945, 8, 17))
        self.assertEqual(v.parse_tanggal("1945-08-17"), date(1945, 8, 17))
        with self.assertRaises(ValueError):
            v.parse_tanggal("31-02-2026")
        with self.assertRaises(ValueError):
            v.parse_tanggal("01-01-1850")
        with self.assertRaises(TypeError):
            v.parse_tanggal(19450817)


if __name__ == "__main__":
    unittest.main()