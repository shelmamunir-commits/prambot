import unittest
from app import app


class TestWebRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_pages_get(self):
        """Verifikasi semua halaman utama dapat diakses via GET."""
        for path in ['/', '/dashboard', '/hitung', '/jodoh', '/hari-baik']:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, f"Gagal akses {path}")

    def test_post_hitung_weton(self):
        """Verifikasi kalkulasi weton lengkap POST menghasilkan output Ki-Demang & Primbon.com."""
        response = self.client.post('/hitung', data={
            'nama': 'Raden Sukarno',
            'tanggal_lahir': '1945-08-17'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Jumat', html)
        self.assertIn('Legi', html)
        self.assertIn('Manahil', html)
        self.assertIn('Paningron', html)  # Sadwara
        self.assertIn('Yama', html)       # Hastawara
        self.assertIn('Tulus', html)      # Sangawara
        self.assertIn('Aras Tuding', html) # Paarasan
        self.assertIn('Sanggar Waringin', html) # Rakam
        self.assertIn('Pal Srigati', html) # Pal Srigati

    def test_post_jodoh(self):
        """Verifikasi pencocokan jodoh multimetode."""
        response = self.client.post('/jodoh', data={
            'nama_a': 'Rama',
            'tanggal_a': '1995-05-10',
            'nama_b': 'Shinta',
            'tanggal_b': '1996-08-20'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Petung 8', html)
        self.assertIn('Pancasuda', html)
        self.assertIn('Petung 5', html)
        self.assertIn('Skor Keselarasan', html)

    def test_post_hari_baik(self):
        """Verifikasi rekomendasi hari baik 30 hari."""
        response = self.client.post('/hari-baik', data={
            'nama': 'Gatotkaca',
            'tanggal_lahir': '1992-03-15',
            'tujuan_acara': 'Pernikahan',
            'tanggal_acara': '2026-12-01'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Tanggal Pilihan Terbaik (8 Hari Terbaik)', html)
        self.assertIn('Daftar Lengkap 30 Hari ke Depan', html)

    def test_unduh_laporan_pdf(self):
        """Verifikasi unduhan laporan PDF setelah menghitung weton."""
        # Hitung weton dulu agar session tersimpan
        self.client.post('/hitung', data={
            'nama': 'Sultan Agung',
            'tanggal_lahir': '1980-01-01'
        })
        # Unduh laporan
        response = self.client.get('/laporan')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/pdf')
        self.assertTrue(response.data.startswith(b'%PDF'))


if __name__ == '__main__':
    unittest.main()
