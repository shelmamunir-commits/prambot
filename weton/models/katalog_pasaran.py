from datetime import date

from utils.konstanta import JANGKAR_INDEKS, JANGKAR_TANGGAL, PASARAN
from utils.validasi import valid_tanggal


class KatalogPasaran:
    """Daftar pasaran dan pencarian pasaran dari tanggal."""

    def __init__(self):
        self._daftar_pasaran: list[str] = list(PASARAN)

    @property
    def daftar_pasaran(self) -> list[str]:
        return list(self._daftar_pasaran)

    def cari_pasaran(self, tanggal: date) -> str:
        if not valid_tanggal(tanggal):
            raise ValueError("Tanggal tidak valid.")
        selisih = (tanggal - JANGKAR_TANGGAL).days
        indeks = (JANGKAR_INDEKS + selisih) % len(self._daftar_pasaran)
        return self._daftar_pasaran[indeks]
