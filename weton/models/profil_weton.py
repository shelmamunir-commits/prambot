from datetime import date
from typing import Optional

from utils.kalender import nama_hari
from utils.konstanta import NILAI_HARI, NILAI_PASARAN
from utils.validasi import valid_hari, valid_nama, valid_pasaran

from .katalog_pasaran import KatalogPasaran
from .komponen_neptu import KomponenNeptu


class ProfilWeton:
    """Hasil weton seseorang.

    Menyimpan nama_pengguna sebagai str (bukan objek Pengguna) sehingga
    tidak ada circular import dengan models.pengguna.
    """

    def __init__(self, nama_pengguna: str, hari: str, pasaran: str):
        if not valid_nama(nama_pengguna):
            raise ValueError(f"Nama tidak valid: {nama_pengguna!r}")
        if not valid_hari(hari):
            raise ValueError(f"Hari tidak dikenal: {hari!r}")
        if not valid_pasaran(pasaran):
            raise ValueError(f"Pasaran tidak dikenal: {pasaran!r}")
        self._nama_pengguna = nama_pengguna.strip()
        self._hari = hari
        self._pasaran = pasaran
        # COMPOSITION: KomponenNeptu dibuat dan dimiliki di dalam profil
        self._neptu = KomponenNeptu(NILAI_HARI[hari], NILAI_PASARAN[pasaran])

    @classmethod
    def dari_tanggal(cls, nama_pengguna: str, tanggal: date,
                     katalog: Optional[KatalogPasaran] = None) -> "ProfilWeton":
        katalog = katalog or KatalogPasaran()
        return cls(nama_pengguna, nama_hari(tanggal), katalog.cari_pasaran(tanggal))

    @property
    def nama_pengguna(self) -> str:
        return self._nama_pengguna

    @property
    def hari(self) -> str:
        return self._hari

    @property
    def pasaran(self) -> str:
        return self._pasaran

    @property
    def neptu(self) -> KomponenNeptu:
        return self._neptu

    def get_detail_weton(self) -> str:
        return f"{self._hari} {self._pasaran} (neptu {self._neptu.total_neptu()})"

    def __str__(self):
        return f"{self._nama_pengguna}: {self.get_detail_weton()}"

    def __repr__(self):
        return (f"ProfilWeton({self._nama_pengguna!r}, "
                f"{self._hari!r}, {self._pasaran!r})")
