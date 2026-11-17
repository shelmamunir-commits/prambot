from datetime import date

from utils.konstanta import JANGKAR_INDEKS, JANGKAR_TANGGAL, PASARAN
from utils.validasi import valid_tanggal


class KatalogPasaran:
    """Daftar pasaran dan pencarian pasaran dari tanggal."""

    def __init__(self):
        self._daftar_pasaran: list[str] = list(PASARAN)
        if not self._daftar_pasaran:
            raise ValueError("Daftar pasaran tidak boleh kosong.")

    @property
    def daftar_pasaran(self) -> list[str]:
        return list(self._daftar_pasaran)

    def cari_pasaran(self, tanggal: date) -> str:
        # valid_tanggal akan melempar TypeError atau ValueError jika tanggal tidak sesuai
        valid_tanggal(tanggal)

        try:
            selisih = (tanggal - JANGKAR_TANGGAL).days
            indeks = (JANGKAR_INDEKS + selisih) % len(self._daftar_pasaran)
            return self._daftar_pasaran[indeks]
        except TypeError as err:
            raise TypeError(f"Tipe data tanggal jangkar tidak valid: {err}")
        except ZeroDivisionError:
            raise ZeroDivisionError("Jumlah daftar pasaran bernilai nol sehingga pembagian modulo gagal.")
        except IndexError:
            raise IndexError("Indeks pasaran berada di luar jangkauan daftar pasaran.")