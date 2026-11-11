import unittest
from datetime import date

from models import KatalogPasaran, KomponenNeptu, Pengguna, ProfilWeton


class TestPasaran(unittest.TestCase):
    """Tanggal acuan dicocokkan dengan kalender Jawa yang diterbitkan."""

    def setUp(self):
        self.katalog = KatalogPasaran()

    def test_jangkar_1945(self):
        p = ProfilWeton.dari_tanggal("Soekarno", date(1945, 8, 17), self.katalog)
        self.assertEqual((p.hari, p.pasaran), ("Jumat", "Legi"))

    def test_agustus_2025(self):
        kasus = {
            date(2025, 8, 1): ("Jumat", "Kliwon"),
            date(2025, 8, 9): ("Sabtu", "Pon"),
            date(2025, 8, 17): ("Minggu", "Legi"),
            date(2025, 8, 22): ("Jumat", "Legi"),
        }
        for tgl, (hari, pasaran) in kasus.items():
            p = ProfilWeton.dari_tanggal("Uji", tgl, self.katalog)
            self.assertEqual((p.hari, p.pasaran), (hari, pasaran), tgl)

    def test_neptu(self):
        p = ProfilWeton("Uji", "Kamis", "Pon")
        self.assertEqual(p.neptu.total_neptu(), 15)
        self.assertEqual(p.get_detail_weton(), "Kamis Pon (neptu 15)")


class TestKomponenNeptu(unittest.TestCase):
    def test_operator(self):
        a, b = KomponenNeptu(4, 8), KomponenNeptu(7, 4)
        self.assertEqual(a + b, 23)
        self.assertEqual(sum([a, b]), 23)
        self.assertTrue(b < a)
        self.assertTrue(a >= b)
        self.assertEqual(a, KomponenNeptu(8, 4))

    def test_tipe_salah(self):
        with self.assertRaises(TypeError):
            KomponenNeptu(4, 8) + "x"


class TestPengguna(unittest.TestCase):
    def test_buat_profil(self):
        u = Pengguna("Rina", date(2003, 5, 17))
        p = u.buat_profil()
        self.assertEqual(u.daftar_profil, [p])

    def test_tanggal_tidak_valid(self):
        with self.assertRaises(ValueError):
            Pengguna("Rina", date(1500, 1, 1))


if __name__ == "__main__":
    unittest.main()
