# Prambot

Aplikasi perhitungan weton Jawa (neptu, jodoh/Pancasuda, hari baik) dan
cetak laporan PDF. Dibuat dengan Python berdasarkan class diagram Prambot.

## Menjalankan
    pip install -r requirements.txt
    python main.py            # menu interaktif
    python main.py --demo     # demo polimorfisme otomatis
    python -m unittest discover -s tests

## Struktur
- models/    : Pengguna, ProfilWeton, KomponenNeptu, KatalogPasaran
- services/  : PerhitunganWeton (ABC), KalkulatorJodoh, KalkulatorHariBaik, CetakLaporanPrimbon
- utils/     : validasi, kalender, konstanta (semua tabel primbon)
- tests/     : unit test

## Rumus
- Neptu = nilai_hari + nilai_pasaran
- Pasaran dihitung dari jangkar 17-08-1945 = Jumat Legi (siklus 5 hari)
- Jodoh: (neptu A + neptu B) mod 7, sisa 0 dihitung 7 -> Pancasuda
- Hari baik: (neptu profil + neptu hari acara) mod 5 -> Sri/Lungguh/Gedhong/Lara/Pati

Tafsir primbon bervariasi antar sumber; ubah tabel di utils/konstanta.py bila perlu.
