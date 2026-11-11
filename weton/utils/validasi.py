"""Fungsi validasi input yang dipakai models, services, dan main."""
import re
from datetime import date, datetime

from .konstanta import NILAI_HARI, NILAI_PASARAN

TAHUN_MIN = 1900
TAHUN_MAKS = 2100
PANJANG_NAMA_MAKS = 50
_POLA_NAMA = re.compile(r"^[A-Za-z][A-Za-z .'\-]*$")


def valid_nama(nama: str) -> bool:
    return (isinstance(nama, str)
            and 0 < len(nama.strip()) <= PANJANG_NAMA_MAKS
            and bool(_POLA_NAMA.match(nama.strip())))


def valid_tanggal(tanggal: date) -> bool:
    return (isinstance(tanggal, date)
            and TAHUN_MIN <= tanggal.year <= TAHUN_MAKS)


def valid_hari(hari: str) -> bool:
    return hari in NILAI_HARI


def valid_pasaran(pasaran: str) -> bool:
    return pasaran in NILAI_PASARAN


def valid_tujuan(tujuan: str) -> bool:
    return isinstance(tujuan, str) and bool(tujuan.strip())


def parse_tanggal(teks: str) -> date:
    """Ubah 'YYYY-MM-DD' atau 'DD-MM-YYYY' menjadi date.

    Raises ValueError jika format salah atau tahun di luar jangkauan.
    """
    teks = teks.strip().replace("/", "-")
    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            hasil = datetime.strptime(teks, fmt).date()
        except ValueError:
            continue
        if not valid_tanggal(hasil):
            raise ValueError(f"Tahun harus {TAHUN_MIN}-{TAHUN_MAKS}.")
        return hasil
    raise ValueError("Format tanggal harus DD-MM-YYYY atau YYYY-MM-DD.")


# Hanya dijalankan jika file ini dieksekusi langsung
if __name__ == "__main__":
    print("Uji cepat modul validasi:")
    print(valid_nama("Rina"), valid_tanggal(date(2000, 1, 1)),
          valid_hari("Senin"), valid_pasaran("Kliwon"))
    print(parse_tanggal("17-08-1945"))
