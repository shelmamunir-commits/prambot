"""Fungsi validasi input yang dipakai models, services, dan main."""
import re
from datetime import date, datetime

from .konstanta import NILAI_HARI, NILAI_PASARAN

TAHUN_MIN = 1900
TAHUN_MAKS = 2100
PANJANG_NAMA_MAKS = 50
_POLA_NAMA = re.compile(r"^[A-Za-z][A-Za-z .'\-]*$")


def valid_nama(nama: str) -> bool:
    if not isinstance(nama, str):
        raise TypeError("Nama harus berupa teks (string).")
    nama_bersih = nama.strip()
    if not nama_bersih:
        raise ValueError("Nama tidak boleh kosong.")
    if len(nama_bersih) > PANJANG_NAMA_MAKS:
        raise ValueError(f"Nama maksimal {PANJANG_NAMA_MAKS} karakter.")
    if not _POLA_NAMA.match(nama_bersih):
        raise ValueError("Nama hanya boleh mengandung huruf, spasi, titik, tanda petik, atau tanda hubung.")
    return True


def valid_tanggal(tanggal: date) -> bool:
    if not isinstance(tanggal, date):
        raise TypeError("Objek tanggal harus bertipe datetime.date.")
    if not (TAHUN_MIN <= tanggal.year <= TAHUN_MAKS):
        raise ValueError(f"Tahun harus berada di antara {TAHUN_MIN} hingga {TAHUN_MAKS}.")
    return True


def valid_hari(hari: str) -> bool:
    if not isinstance(hari, str) or hari not in NILAI_HARI:
        raise KeyError(f"Hari '{hari}' tidak valid atau tidak ditemukan di konstanta.")
    return True


def valid_pasaran(pasaran: str) -> bool:
    if not isinstance(pasaran, str) or pasaran not in NILAI_PASARAN:
        raise KeyError(f"Pasaran '{pasaran}' tidak valid atau tidak ditemukan di konstanta.")
    return True


def valid_tujuan(tujuan: str) -> bool:
    if not isinstance(tujuan, str) or not tujuan.strip():
        raise ValueError("Tujuan perhitungan tidak boleh kosong.")
    return True


def parse_tanggal(teks: str) -> date:
    """Ubah 'YYYY-MM-DD' atau 'DD-MM-YYYY' menjadi date.

    Raises TypeError jika input bukan string.
    Raises ValueError jika format salah atau tahun di luar jangkauan.
    """
    if not isinstance(teks, str):
        raise TypeError("Input tanggal harus berupa teks (string).")

    teks = teks.strip().replace("/", "-")
    if not teks:
        raise ValueError("Tanggal lahir tidak boleh kosong.")

    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            hasil = datetime.strptime(teks, fmt).date()
        except ValueError:
            continue
        # Validasi rentang tahun menggunakan valid_tanggal
        valid_tanggal(hasil)
        return hasil

    raise ValueError("Format tanggal tidak valid. Gunakan DD-MM-YYYY atau YYYY-MM-DD.")


# Hanya dijalankan jika file ini dieksekusi langsung
if __name__ == "__main__":
    print("Uji cepat modul validasi:")
    try:
        print(valid_nama("Rina"), valid_tanggal(date(2000, 1, 1)),
              valid_hari("Senin"), valid_pasaran("Kliwon"))
        print(parse_tanggal("17-08-1945"))
        # Tes memicu error
        print(parse_tanggal("31-02-2026"))
    except (TypeError, ValueError, KeyError) as err:
        print(f"Error tertangkap dengan aman: {err}")