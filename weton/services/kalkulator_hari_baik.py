from datetime import date, timedelta

from models import KatalogPasaran, ProfilWeton
from utils.konstanta import (HARI_BAIK_LIMA, PEMBAGI_HARI_BAIK, WATAK_HARI,
                             WATAK_PASARAN)
from utils.validasi import valid_tanggal, valid_tujuan

from .perhitungan_weton import PerhitunganWeton


class KalkulatorHariBaik(PerhitunganWeton):
    """Menilai tanggal acara terhadap weton pemilik profil."""

    def __init__(self, id_kalkulasi: str, tanggal_lahir: date,
                 profil: ProfilWeton, katalog: KatalogPasaran,
                 tanggal_acara: date, tujuan_acara: str):
        super().__init__(id_kalkulasi, tanggal_lahir, profil, katalog)
        if not valid_tanggal(tanggal_acara):
            raise ValueError("Tanggal acara tidak valid.")
        if not valid_tujuan(tujuan_acara):
            raise ValueError("Tujuan acara wajib diisi.")
        self._tanggal_acara = tanggal_acara
        self._tujuan_acara = tujuan_acara.strip()
        self._profil_acara = ProfilWeton.dari_tanggal("Acara", tanggal_acara, katalog)

    # --- override method abstrak ---
    def hitung_neptu(self) -> int:
        """Neptu weton pada tanggal acara."""
        return self._profil_acara.neptu.total_neptu()

    def analisis_karakter(self) -> str:
        p = self._profil_acara
        return (f"Hari acara {p.hari} {p.pasaran}: "
                f"{WATAK_HARI[p.hari]}; {WATAK_PASARAN[p.pasaran]}")

    # --- method khusus subclass ---
    def _sisa(self, profil_acara: ProfilWeton) -> int:
        return (self._profil.neptu + profil_acara.neptu) % PEMBAGI_HARI_BAIK

    def analisis_hari_baik(self) -> str:
        sisa = self._sisa(self._profil_acara)
        nama, baik, makna = HARI_BAIK_LIMA[sisa]
        penilaian = "BAIK" if baik else "KURANG BAIK"
        return (f"Acara '{self._tujuan_acara}' pada {self._tanggal_acara:%d-%m-%Y} "
                f"({self._profil_acara.hari} {self._profil_acara.pasaran}): "
                f"{nama} - {penilaian}. {makna}")

    def rekomendasi(self, mulai: date, rentang: int = 30) -> list[tuple[date, str, str]]:
        """Daftar (tanggal, weton, nama) hari baik dalam `rentang` hari."""
        hasil = []
        for i in range(rentang):
            tgl = mulai + timedelta(days=i)
            if not valid_tanggal(tgl):
                break
            kandidat = ProfilWeton.dari_tanggal("Acara", tgl, self._katalog)
            nama, baik, _ = HARI_BAIK_LIMA[self._sisa(kandidat)]
            if baik:
                hasil.append((tgl, f"{kandidat.hari} {kandidat.pasaran}", nama))
        return hasil
