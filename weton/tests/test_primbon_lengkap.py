import unittest
from datetime import date
from services.primbon_lengkap import PrimbonLengkap

class TestPrimbonLengkap(unittest.TestCase):

    def test_proklamasi_17_agustus_1945(self):
        """Verifikasi data historis 17 Agustus 1945 sesuai rujukan Ki-Demang & Primbon Jawa."""
        res = PrimbonLengkap.profil_weton_lengkap('Proklamasi', date(1945, 8, 17))
        pw = res['pawukon']
        
        self.assertEqual(pw['hari'], 'Jumat')
        self.assertEqual(pw['pasaran'], 'Legi')
        self.assertEqual(pw['total_neptu'], 11)
        self.assertEqual(pw['wuku'], 'Manahil')
        self.assertEqual(pw['sadwara']['nama'], 'Paningron')
        self.assertEqual(pw['hastawara']['nama'], 'Yama')
        self.assertEqual(pw['sangawara']['nama'], 'Tulus')
        self.assertEqual(pw['paarasan']['nama'], 'Aras Tuding')
        self.assertEqual(pw['rakam']['nama'], 'Sanggar Waringin')
        self.assertIn(pw['pancasuda']['nama'], ['Satrya Wirang', 'Satria Wirang'])
        self.assertIn('jujur', res['watak_lengkap'].lower())
        self.assertTrue(len(res['pal_srigati']) > 0)

    def test_jodoh_multimetode(self):
        """Uji analisis jodoh multimetode."""
        res = PrimbonLengkap.analisis_jodoh_komprehensif('Pria', date(1995, 1, 1), 'Wanita', date(1996, 2, 2))
        self.assertIn('metode_8', res)
        self.assertIn('metode_7', res)
        self.assertIn('metode_5', res)
        self.assertTrue(0 <= res['skor'] <= 100)

    def test_rekomendasi_hari_baik_30(self):
        """Uji rekomendasi hari baik 30 hari."""
        res = PrimbonLengkap.rekomendasi_hari_baik_30('Budi', date(1990, 5, 5), date(2026, 11, 11), 'Pernikahan')
        self.assertEqual(len(res['daftar_30']), 30)
        self.assertTrue(len(res['daftar_terbaik']) > 0)

    def test_render_pdf_lengkap(self):
        """Uji ekspor PDF dengan dataset primbon lengkap."""
        import os, tempfile
        from models import ProfilWeton
        from services.cetak_laporan_primbon import CetakLaporanPrimbon

        res = PrimbonLengkap.profil_weton_lengkap('Raden Wijaya', date(1992, 4, 15))
        profil = ProfilWeton('Raden Wijaya', res['pawukon']['hari'], res['pawukon']['pasaran'])
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "laporan_uji.pdf")
            CetakLaporanPrimbon().render_pdf(profil, path, data_lengkap=res)
            self.assertTrue(os.path.exists(path))
            with open(path, "rb") as f:
                self.assertEqual(f.read(4), b"%PDF")

if __name__ == '__main__':
    unittest.main()
