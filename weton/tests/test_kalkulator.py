import os
import tempfile
import unittest
from datetime import date

from models import KatalogPasaran, ProfilWeton
from services import (CetakLaporanPrimbon, KalkulatorHariBaik, KalkulatorJodoh,
                      PerhitunganWeton)


class TestKalkulator(unittest.TestCase):
    def setUp(self):
        self.katalog = KatalogPasaran()
        self.lahir = date(1990, 1, 1)
        self.profil = ProfilWeton("Hartono", "Senin", "Kliwon")  # neptu 12

    def test_abstrak_tidak_bisa_dibuat(self):
        with self.assertRaises(TypeError):
            PerhitunganWeton("X", self.lahir, self.profil, self.katalog)

    def test_jodoh_contoh_artikel(self):
        # Senin Kliwon (12) + Rabu Wage (11) = 23 -> 23 % 7 = 2 -> Tunggak Semi
        k = KalkulatorJodoh("KJ", self.lahir, self.profil, self.katalog,
                            date(2025, 8, 20), "Hartini")  # Rabu Wage
        self.assertEqual(k.profil_pasangan.get_detail_weton(), "Rabu Wage (neptu 11)")
        self.assertEqual(k.hitung_neptu(), 23)
        self.assertEqual(k.sisa_pancasuda(), 2)
        self.assertIn("Tunggak Semi", k.analisis_keselarasan())

    def test_sisa_nol_menjadi_tujuh(self):
        # Jumat Kliwon (14) + Kamis Wage? atur manual: 14 + 14 = 28 -> 0 -> 7
        profil = ProfilWeton("A", "Jumat", "Kliwon")
        k = KalkulatorJodoh("KJ", self.lahir, profil, self.katalog,
                            date(2025, 8, 1), "B")  # Jumat Kliwon
        self.assertEqual(k.hitung_neptu(), 28)
        self.assertEqual(k.sisa_pancasuda(), 7)

    def test_overloading_singledispatch(self):
        k = KalkulatorJodoh("KJ", self.lahir, self.profil, self.katalog,
                            date(2025, 8, 20))
        via_tanggal = k.hitung_dengan(date(2025, 8, 20))
        via_profil = k.hitung_dengan(ProfilWeton("P", "Rabu", "Wage"))
        self.assertEqual(via_tanggal, via_profil)
        with self.assertRaises(TypeError):
            k.hitung_dengan("2025-08-20")

    def test_polimorfisme(self):
        daftar = [
            KalkulatorJodoh("KJ", self.lahir, self.profil, self.katalog,
                            date(2025, 8, 20)),
            KalkulatorHariBaik("KH", self.lahir, self.profil, self.katalog,
                               date(2025, 8, 17), "usaha"),
        ]
        hasil = {type(k).__name__: k.hitung_neptu() for k in daftar}
        self.assertEqual(hasil["KalkulatorJodoh"], 23)
        self.assertEqual(hasil["KalkulatorHariBaik"], 10)  # Minggu Legi
        for k in daftar:
            self.assertIsInstance(k, PerhitunganWeton)
            self.assertIsInstance(k.ringkasan(), str)

    def test_hari_baik(self):
        # 12 + 10 = 22 -> sisa 2 -> Lungguh (baik)
        k = KalkulatorHariBaik("KH", self.lahir, self.profil, self.katalog,
                               date(2025, 8, 17), "usaha")
        self.assertIn("Lungguh", k.analisis_hari_baik())
        daftar = k.rekomendasi(date(2025, 8, 1), 10)
        self.assertTrue(all(len(x) == 3 for x in daftar))

    def test_cetak_pdf(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "x.pdf")
            CetakLaporanPrimbon().render_pdf(self.profil, path)
            with open(path, "rb") as f:
                self.assertEqual(f.read(4), b"%PDF")


if __name__ == "__main__":
    unittest.main()
